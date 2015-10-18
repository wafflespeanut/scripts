execfile("Download MP3s.py")
from PIL import Image
import os

path = os.path.expanduser('~/Desktop/Dropbox/Philographics/')
link = "http://geniscarreras.com/philographics"

def download():
    if not os.path.exists(path):
        mkdir(path)
    for image in urls(link, 'jpg', '//img/@data-src'):
        name = image.split('/')[-1]
        print 'Downloading', name, '...'
        urlretrieve(image, path + name)
        print 'Processing...'
        process(path + name, name)

def process(image, name):       # Some experiment for making wallpapers from those philographics
    img = Image.open(image)
    width, height = img.size
    r, g, b = img.getpixel((width - 1, height - 1))             # Pick color
    width = int(height * float(1366) / 768)
    newImg = Image.new(img.mode, (width, height), (r, g, b))
    offset = (newImg.size[0] - img.size[0]) / 2                 # Position: center
    newImg.paste(img, (offset, 0))
    newImg.save(path + name)
