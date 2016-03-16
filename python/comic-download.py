import os, shutil, sys, re, urllib, lxml.html

# for downloading comics (one at a time!)

try:
    link = sys.argv[1]
    main_response = urllib.urlopen(link).read()
    for match in re.finditer('<a href=[\'"](.*?)[\'"].*?</a>', main_response):
        l = match.group(1)
        if l.count('/') > 3 and '?' not in l:
            print 'Crawling into %s...' % l
            page_response = urllib.urlopen(l).read()
            dom = lxml.html.fromstring(page_response)
            for sub_link in (l for l in dom.xpath('//a/@href') if l.endswith('.zip')):
                archive = os.path.expanduser('~/Desktop/%s' % sub_link.split('/')[-1])
                if not os.path.exists(archive):
                    print 'Downloading %s... (%s bytes)' % (sub_link, urllib.urlopen(sub_link).info()['Content-Length'])
                    try:
                        urllib.urlretrieve(sub_link, archive)
                    except (Exception, KeyboardInterrupt):
                        print 'Interrupted!'
                        if os.path.exists(archive):
                            os.remove(archive)
                        sys.exit()
except KeyboardInterrupt:
    pass
