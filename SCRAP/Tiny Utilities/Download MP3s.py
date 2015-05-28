from urllib import *
from os import *
import lxml.html

links = []
path = "C:\\Users\\Waffles Crazy Peanut\\Desktop\\TEMP\\"

# I used to download embedded MP3 soundtracks with this...

def urls(link, what = 'mp3', tag = '//a/@href'):
    response = urlopen(link).read()               # Whole page-source is in here!
    dom = lxml.html.fromstring(response)
    return [l for l in dom.xpath(tag) if '#' not in l and what in l]

def get():
    for link in links:
       folder = link.split('/')[-1]
        try:
            mkdir(path + folder)
        except WindowsError:
            print "\n[FOLDER] %s already exists! \n" % folder
        for i in urls(link):
            try:
                dlink = urls(i)[0]
                name = dlink.split('/')[-1]
                if name in listdir(path + folder):
                    print "[File] %s already exists! " % name      # path.getsize() can also be used
                    if stat(path + folder + '\\' + name).st_size == int(urlopen(l).info()['Content - Length']):
                        continue
                    else:
                        s = str(raw_input("\tFile has different size! Overwrite (y/n)? "))
                        if s == 'y':
                            print "Downloading", dlink, "..."
                            urlretrieve(l, path + folder + '\\' + name)
                            continue
                        else:
                            print "\t[File] %s skipped! " % name
                            continue
                print "Downloading", dlink, "..."
                urlretrieve(l, path + folder + '\\' + name)
            except (IOError, KeyboardInterrupt):
                print '\t[File] %s skipped! ' % name
                if path.exists(path + folder + '\\' + name):
                    remove(path + folder + '\\' + name)
                continue
