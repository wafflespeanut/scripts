from PIL import Image
from multiprocessing import Process, Queue

import argparse
import gdal2tiles
import multiprocessing
import os
import shutil

INDEX_HTML = '''<!DOCTYPE html>\n<html lang="en">\n  <head>\n  <title>Mosaic</title>\n  <meta charset="utf-8" />\n  <meta http-equiv='imagetoolbar' content='no'/>\n  <style type="text/css">\n    html, body {{ overflow: hidden; padding: 0; height: 100%; width: 100%; font-family: 'Lucida Grande',Geneva,Arial,Verdana,sans-serif; }}\n    body {{ margin: 10px; background: #000; }}\n    .olImageLoadError {{ display: none; }}\n    .olControlLayerSwitcher .layersDiv {{ border-radius: 10px 0 0 10px; }}\n  </style>\n<script src="./OpenLayers-2.12.js"></script>\n<script>\n  var map;\n  var mapBounds = new OpenLayers.Bounds(0.0, -{height}.0, {width}.0, 0.0);\n  var mapMinZoom = {minZoom};\n  var mapMaxZoom = {maxZoom};\n  var emptyTileURL = "./tile-none.png";\n  OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;\n\n  function init(){{\n    map = new OpenLayers.Map({{\n      div: "map",\n      controls: [],\n      maxExtent: new OpenLayers.Bounds(0.0, -{height}.0, {width}.0, 0.0),\n      maxResolution: 64.000000,\n      numZoomLevels: 8\n    }});\n\n    var layer = new OpenLayers.Layer.TMS("TMS Layer", "", {{\n      serviceVersion: '.',\n      layername: './tiles',\n      type: 'jpg',\n      getURL: getURL,\n    }});\n\n    map.addLayer(layer);\n    map.zoomToExtent(mapBounds);\n\n    map.addControls([new OpenLayers.Control.Navigation()]);\n  }}\n\n  function getURL(bounds) {{\n    bounds = this.adjustBounds(bounds);\n    var res = this.getServerResolution();\n    var x = Math.round((bounds.left - this.tileOrigin.lon) / (res * this.tileSize.w));\n    var y = Math.round((bounds.bottom - this.tileOrigin.lat) / (res * this.tileSize.h));\n    var z = this.getServerZoom();\n    var path = this.serviceVersion + "/" + this.layername + "/" + z + "/" + x + "/" + y + "." + this.type;\n    var url = this.url;\n    if (OpenLayers.Util.isArray(url)) {{\n      url = this.selectUrl(path, url);\n    }}\n\n    if (mapBounds.intersectsBounds(bounds) && (z >= mapMinZoom) && (z <= mapMaxZoom)) {{\n      return url + path;\n    }} else {{\n      return emptyTileURL;\n    }}\n  }}\n\n  function getWindowHeight() {{\n    if (self.innerHeight) return self.innerHeight;\n    if (document.documentElement && document.documentElement.clientHeight)\n      return document.documentElement.clientHeight;\n    if (document.body) return document.body.clientHeight;\n      return 0;\n  }}\n\n  function getWindowWidth() {{\n    if (self.innerWidth) return self.innerWidth;\n    if (document.documentElement && document.documentElement.clientWidth)\n      return document.documentElement.clientWidth;\n    if (document.body) return document.body.clientWidth;\n      return 0;\n  }}\n\n  function resize() {{\n    var map = document.getElementById("map");\n    map.style.height = (getWindowHeight()-20) + "px";\n    map.style.width = (getWindowWidth()-20) + "px";\n    if (map.updateSize) {{\n      map.updateSize();\n    }}\n  }}\n\n  window.onresize = function() {{ resize(); }};\n\n  </script>\n</head>\n<body onload="init()">\n  <div id="map"></div>\n  <script type="text/javascript" >resize()</script>\n</body>\n</html>\n'''  # noqa: F401
NUM_CPUS = os.environ.get('NUM_JOBS', multiprocessing.cpu_count())
MIN_ZOOM = 1
MAX_ZOOM = 7

Image.MAX_IMAGE_PIXELS = None


class TileFinder:
    def __init__(self, tiles):
        self.tiles = tiles

    def get_best_tile_index(self, patch_img):
        '''Find the index of the best tile matching the given image patch.'''
        min_dist = float('inf')
        tile_idx = 0

        for idx, tile in enumerate(self.tiles):
            dist = self.__get_dist(patch_img, tile, min_dist)
            if dist < min_dist:
                min_dist = dist
                tile_idx = idx

        return tile_idx

    def __get_dist(self, t1, t2, max_value):
        dist = 0
        for i in range(len(t1)):
            # Compute Euclidean disatnce.
            dist += (
                (t1[i][0] - t2[i][0])**2 +
                (t1[i][1] - t2[i][1])**2 +
                (t1[i][2] - t2[i][2])**2)
            if dist > max_value:
                return dist
        return dist


# Photomosaic builder modified from https://github.com/codebox/mosaic
class MosaicBuilder:
    def __init__(self, img, out_path, tile_size=150,
                 compare_tile_size=25, resize_factor=20):
        img = img.convert('RGB')
        self.out_path = out_path
        self.counter = 0
        self.tile_size = tile_size
        self.compare_tile_size = max(compare_tile_size, 1)
        self.resize_factor = resize_factor
        self.compare_ratio = self.tile_size / self.compare_tile_size
        self.actual_tiles = []
        self.compare_tiles = []

        print('Adjusting image and initializing mosaic.')
        w = img.size[0] * self.resize_factor
        h = img.size[1] * self.resize_factor
        self.image = img.resize((w, h), Image.ANTIALIAS)
        print(f'New size: {self.image.size[0]}x{self.image.size[1]}')
        w_extra, h_extra = (w % self.tile_size) / 2, (h % self.tile_size) / 2
        # Crop if the size isn't a multiple of the tiles.
        if w_extra or h_extra:
            w_end, h_end = w - w_extra, h - h_extra
            self.image = self.image.crop((w_extra, h_extra, w_end, h_end))

        self.num_x_tiles = int(self.image.size[0] / self.tile_size)
        self.num_y_tiles = int(self.image.size[1] / self.tile_size)
        self.num_tiles = self.num_x_tiles * self.num_y_tiles
        print('Estimated tiles:', self.num_tiles)

        self.compare_image = self.image.resize(
            (int(w / self.compare_ratio), int(h / self.compare_ratio)),
            Image.ANTIALIAS
        )

    def collect_tiles(self, tiles_dir=None):
        '''Collect tile images by recursively walking the given path.'''
        if tiles_dir is None:
            return

        for parent, _, files in os.walk(tiles_dir):
            for tile in files:
                tile_path = os.path.join(parent, tile)
                tile, compare_tile = self.__process_tile(tile_path)
                if not tile:
                    continue

                # We're passing lists so that we can serialize in IPC.
                self.actual_tiles.append(list(tile.getdata()))
                self.compare_tiles.append(list(compare_tile.getdata()))
        print(' ' * 40, end='\r')
        print('Processed %d tiles.' % len(self.actual_tiles))

    def build_mosaic(self):
        '''Builds mosaic for the image from the collected tiles.'''
        num_workers = NUM_CPUS - 1
        in_queue = Queue(num_workers)
        out_queue = Queue()

        proc = Process(target=MosaicBuilder.__build,
                       args=(self.image.mode, self.image.size, self.out_path,
                             self.actual_tiles, self.tile_size, out_queue))
        proc.start()

        print('Spawning', num_workers, 'workers for building mosaic.')
        for i in range(num_workers):
            Process(target=MosaicBuilder.__find,
                    args=(in_queue, out_queue, self.compare_tiles)).start()

        try:
            self.__send_chunks(in_queue)
        except KeyboardInterrupt:
            print('Received signal. Shutting down workers.')

        for _ in range(num_workers):
            in_queue.put((None, None))

        proc.join()

    def __build(mode, size, out_path, tiles, tile_size, out_queue):
        mosaic = Image.new(mode, size)
        workers = NUM_CPUS - 1
        while workers > 0:
            coords, idx = out_queue.get()
            if coords is None:
                workers -= 1
                continue

            tile = tiles[idx]
            img = Image.new('RGB', (tile_size, tile_size))
            img.putdata(tile)
            mosaic.paste(img, coords)

        mosaic.save(out_path)

    def __find(in_queue, out_queue, tiles):
        finder = TileFinder(tiles)
        while True:
            data, coords = in_queue.get()
            if data is None:
                break
            idx = finder.get_best_tile_index(data)
            out_queue.put((coords, idx))

        out_queue.put((None, None))

    def __send_chunks(self, in_queue):
        for x in range(self.num_x_tiles):
            for y in range(self.num_y_tiles):
                large_box = (x * self.tile_size,
                             y * self.tile_size,
                             (x + 1) * self.tile_size,
                             (y + 1) * self.tile_size)
                small_box = (x * self.compare_tile_size,
                             y * self.compare_tile_size,
                             (x + 1) * self.compare_tile_size,
                             (y + 1) * self.compare_tile_size)
                in_queue.put(
                    # Again, list for IPC serialization.
                    (list(self.compare_image.crop(small_box).getdata()),
                     large_box))
                self.__update_progress()

    def __process_tile(self, path):
        try:
            img = Image.open(path).convert('RGB')
        except Exception:
            return None, None

        print('  Processing tile {:40.40}'.format(os.path.basename(path)), flush=True, end='\r')
        w, h = img.size
        min_size = min(w, h)
        w_crop, h_crop = (w - min_size) / 2, (h - min_size) / 2
        img = img.crop((w_crop, h_crop, w - w_crop, h - h_crop))

        return (
            img.resize((self.tile_size, self.tile_size), Image.ANTIALIAS),
            img.resize(
                (self.compare_tile_size, self.compare_tile_size),
                Image.ANTIALIAS,
            )
        )

    def __update_progress(self):
        self.counter += 1
        print("  Progress: {:04.1f}%".format(
            100 * self.counter / self.num_tiles), flush=True, end='\r')


class Tiler:
    def __init__(self, img_path, out_dir):
        self.img = Image.open(img_path)
        self.img_path = img_path
        self.out_dir = out_dir

    def generate(self):
        gdal2tiles.generate_tiles(self.img_path, self.out_dir,
                                  profile='raster',
                                  nb_processes=NUM_CPUS,
                                  resume=True,
                                  zoom=(MIN_ZOOM, MAX_ZOOM))
        os.remove(os.path.join(self.out_dir, 'openlayers.html'))

        print('Removing alpha layer in tiles.')
        for parentDir, _, files in os.walk(self.out_dir):
            for f in files:
                if not f.endswith('.png'):
                    continue

                rel_path = os.path.join(parentDir, f)
                leaf = rel_path[len(self.out_dir):]
                print('  Converting {:40.40}'.format(leaf), flush=True, end='\r')
                im = Image.open(rel_path)
                bg = Image.new('RGB', im.size, (0, 0, 0))
                bg.paste(im, im.split()[-1])
                bg.save(rel_path.replace('.png', '.jpg'))
                os.remove(rel_path)


if __name__ == "__main__":
    script_path = os.path.realpath(__file__)
    assets_path = os.path.join(os.path.dirname(script_path), 'assets')
    assert os.path.exists(assets_path)

    parser = argparse.ArgumentParser(
        description='Generate or tile photomosaic images.')
    parser.add_argument('image', help='Path to input image.')
    parser.add_argument('-s', '--source', metavar='DIR',
                        help='Directory containing source images for mosaic.')
    parser.add_argument(
        '-o', '--output', metavar='FILE',
        help='Mosaic output path (default: obtained from input basename).')
    parser.add_argument('-m', '--mosaic', action='store_true',
                        help='Build mosaic only (skip tiles)')
    parser.add_argument('-t', '--tiles', action='store_true',
                        help='Build tiles only (skip mosaic)')
    options = parser.parse_args()
    if not options.tiles:
        img = Image.open(options.image)

    if not options.source:
        parser.error('--source must be specified for building mosaic.')
    out_path = options.output
    if not out_path:
        base, _ = os.path.splitext(options.image)
        out_path = base + '_mosaic.jpg'

    if not options.tiles:
        builder = MosaicBuilder(img, out_path)
        builder.collect_tiles(options.source)
        builder.build_mosaic()
    if options.mosaic:
        exit()

    workdir = os.path.dirname(out_path)
    tiles_dir = os.path.join(workdir, 'tiles')
    tiler = Tiler(out_path, tiles_dir)
    tiler.generate()

    with open(os.path.join(workdir, 'index.html'), 'w') as fd:
        fd.write(INDEX_HTML.format(
            width=tiler.img.width,
            height=tiler.img.height,
            minZoom=MIN_ZOOM,
            maxZoom=MAX_ZOOM,
        ))
        shutil.copyfile(os.path.join(assets_path, 'none.png'),
                        os.path.join(workdir, 'tile-none.png'))
        shutil.copyfile(os.path.join(assets_path, 'OpenLayers-2.12.js'),
                        os.path.join(workdir, 'OpenLayers-2.12.js'))
