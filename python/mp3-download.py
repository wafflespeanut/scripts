import os, sys, urllib, lxml.html

# I used to download embedded MP3 soundtracks with this...

PATH = os.path.expanduser('~/Desktop/TEMP/')


def find_urls(link, what = '.mp3', tag = '//a/@href'):
    response = urllib.urlopen(link).read()      # page source
    dom = lxml.html.fromstring(response)
    return sorted(set([l for l in dom.xpath(tag) if '#' not in l and l.endswith(what)]))


def mp3_get(link, path):
    dir_path = os.path.join(path, link.split('/')[-1])
    if os.path.exists(dir_path):
        print "\n[FOLDER] %s already exists! \n" % dir_path
    else:
        os.mkdir(dir_path)

    for url in find_urls(link):
        try:
            dlink = find_urls(url)[0]
            name = url.split('/')[-1]
            file_path = os.path.join(dir_path, name)

            while True:
                try:
                    if name in os.listdir(dir_path):
                        file_size = int(urllib.urlopen(dlink).info()['Content-Length'])
                        print "[File] %s already exists!" % name      # path.getsize() can also be used
                        if os.stat(file_path).st_size == file_size:
                            break
                        else:
                            print '[File] %s varies in size. Redownloading...'

                    print "Downloading", dlink, "..."
                    urllib.urlretrieve(dlink, file_path)
                    break
                except:
                    print 'Retrying...'

        except (IOError, KeyboardInterrupt):
            print '\t[File] %s skipped! ' % name
            continue

if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        exit('Requires links to download pages')

    links = map(lambda line: line.strip(), args)

    if not os.path.exists:
        os.mkdir(PATH)

    for link in links:
        mp3_get(link, PATH)
