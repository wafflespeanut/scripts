import urllib
from os import mkdir
import lxml.html
from random import choice

o="C:\\Downloads\\"; link=""

def name():     # Just to put random names to the files!
    s='c'
    for i in range(3): s+=str(choice(range(10)))
    for i in range(3): s+=chr(choice(range(97,123)))
    return s

def urls(link):
    connection=urllib.urlopen(link)
    dom=lxml.html.fromstring(connection.read())
    for l in dom.xpath('//a/@href'):
        if '#' not in l and 'jpg' in l: return l

def getimg(link):       # Grabbing a list of images
    out=o+name()+'//'; mkdir(out)
    for i in range(15):
        l=link+str(i)+'/'
        print "Downloading",l,"..."
        urllib.urlretrieve(urls(l),out+str(i+1)+'.jpg')
