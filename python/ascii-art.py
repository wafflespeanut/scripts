from collections import Counter
from PIL import Image, ImageFilter, ImageFont, ImageDraw, ImageEnhance, ImageOps

import argparse
import cgi
import colorsys
import string

MIN_LEVEL = 80
MAX_LEVEL = 127
GAMMA = 0.78

HTML_PREFIX = '''
<!DOCTYPE html>
<html>
<head>
    <title>ASCII Art</title>
    <style type="text/css">
        #text {
            font-size: 4px;
            font-family: monospace, Courier;
            line-height: 0.4;
        }
    </style>
</head>
<body>
<pre id='text'>
'''

HTML_SUFFIX = '''
</pre>
</body>
</html>
'''

# Level object from https://stackoverflow.com/a/3125421/2313792
class Level(object):
    def __init__(self, min_val, max_val, gamma):
        self.min_value, self.max_value = min_val / 255.0, max_val / 255.0
        self.interval = self.max_value - self.min_value
        self.inv_gamma = 1.0 / gamma

    def level_values(self, band_values):
        h, s, v = colorsys.rgb_to_hsv(*(i / 255.0 for i in band_values))
        if v <= self.min_value:
            v = 0.0
        elif v >= self.max_value:
            v = 1.0
        else:
            v = ((v - self.min_value) / self.interval) ** self.inv_gamma
        return tuple(int(255 * i) for i in colorsys.hsv_to_rgb(h, s, v))


def generate_basic_sketch(image, min_level, max_level, gamma):
    blur_filter = ImageFilter.GaussianBlur(radius=8)
    foreground = image.filter(blur_filter)          # apply gaussian blur
    foreground = ImageOps.invert(foreground)        # invert colors
    image = Image.blend(foreground, image, 0.5)     # blend with 50% opacity (should show the outlines)
    leveller = Level(min_level, max_level, gamma)   # clamp color levels
    data = [leveller.level_values(data) for data in image.getdata()]
    image.putdata(data)
    return image

# Modified from https://github.com/ajalt/pyasciigen/blob/master/asciigen.py
def generate_art(path, given_width=None, brightness=None, contrast=None,
                 min_level=MIN_LEVEL, max_level=MAX_LEVEL, gamma=GAMMA, html=False):
    font = ImageFont.load_default()
    char_width, char_height = font.getsize('X')

    def char_density(c, font=font):
        image = Image.new('1', font.getsize(c), color=255)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), c, font=font)
        return Counter(image.getdata())[0]      # count black pixels

    # sort the characters according to the pixel density of their render
    chars = sorted(string.letters + string.digits + string.punctuation + ' ',
                   key=char_density, reverse=True)

    image = Image.open(path)
    scale = 1
    width, height = image.size
    if given_width is not None:
        scale = float(given_width) / width
        width = given_width

    if contrast is not None:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if brightness is not None:
        image = ImageEnhance.Brightness(image).enhance(brightness)

    # resize the image based on character size and aspect ratio
    height = int(height * scale * char_width / float(char_height))
    image = image.resize((width, height), Image.ANTIALIAS)
    # generate basic sketch to extract the necessary details
    image = generate_basic_sketch(image, min_level, max_level, gamma)
    pixels = image.convert('L').load()

    if html:
        print HTML_PREFIX

    for y in xrange(height):
        s = ''.join(chars[int(pixels[x, y] / 255. * (len(chars) - 1) + 0.5)] for x in xrange(width))
        if html:
            print s
        else:
            print cgi.escape(s) + '<br />\n'

    if html:
        print HTML_SUFFIX


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate ascii art from an image.')
    parser.add_argument('image', help='Image file to read.')
    parser.add_argument('--width', '-w', type=int,
                        help='Width of output text. (Default: width of image)')
    parser.add_argument('--min-level', '-mi', type=int,
                        help='Min clamping value for sketch. (Default: %s)' % MIN_LEVEL)
    parser.add_argument('--max-level', '-mx', type=int,
                        help='Max clamping value for sketch. (Default: %s)' % MAX_LEVEL)
    parser.add_argument('--gamma', '-g', metavar='RATIO', type=float,
                        help='Gamma value for sketch. (Default: %s)' % GAMMA)
    parser.add_argument('--contrast', '-c', metavar='RATIO', type=float,
                        help='Contrast ratio to apply to image.')
    parser.add_argument('--brightness', '-b', metavar='RATIO', type=float,
                        help='Brightness ratio to apply to image.')
    parser.add_argument('--html', '-html', action='store_true',
                        help='Print HTML in stdout')
    parser.set_defaults(min_level=MIN_LEVEL, max_level=MAX_LEVEL, gamma=GAMMA, html=False)
    args = parser.parse_args()

    generate_art(args.image, args.width, args.brightness, args.contrast,
                 args.min_level, args.max_level, args.gamma, args.html)
