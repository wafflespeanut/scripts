import urllib
import lxml.html

def urls(link):
    connection=urllib.urlopen(link)
    dom=lxml.html.fromstring(connection.read())
    for l in dom.xpath('//a/@href'):
        if '#' not in l:
            print l
