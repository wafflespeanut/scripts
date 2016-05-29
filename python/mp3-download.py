import os, urllib, lxml.html

links = ["http://downloads.khinsider.com/game-soundtracks/album/assassin-s-creed-iv-black-flag-the-complete-edition"]
path = os.path.expanduser('~/Desktop/TEMP/')

# I used to download embedded MP3 soundtracks with this...

def urls(link, what = '.mp3', tag = '//a/@href'):
    response = urllib.urlopen(link).read()               # Whole page-source is in here!
    dom = lxml.html.fromstring(response)
    return sorted(set([l for l in dom.xpath(tag) if '#' not in l and l.endswith(what)]))

def mp3_get(save_path = path):
    for link in links:
        dir_path = os.path.join(save_path, link.split('/')[-1])
        if os.path.exists(dir_path):
            print "\n[FOLDER] %s already exists! \n" % dir_path
        else:
            os.mkdir(dir_path)

        for url in urls(link):
            try:
                dlink = urls(url)[0]
                name = url.split('/')[-1]
                file_path = os.path.join(dir_path, name)
                if name in os.listdir(dir_path):
                    print "[File] %s already exists! " % name      # path.getsize() can also be used
                    if os.stat(file_path).st_size == int(urllib.urlopen(dlink).info()['Content-Length']):
                        continue
                    elif raw_input("\tFile has different size! Overwrite (y/n)? ") != 'y':
                        print "\t[File] %s skipped! " % name
                        continue
                print "Downloading", dlink, "..."
                urllib.urlretrieve(dlink, file_path)
            except (IOError, KeyboardInterrupt):
                print '\t[File] %s skipped! ' % name
                if os.path.exists(file_path):
                    os.remove(file_path)
                continue
