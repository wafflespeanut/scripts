from urllib import *
from os import mkdir
import lxml.html
from random import choice

o="C:\\Downloads\\"; links=[]

# I used to download comics with this...

def name():     # Just to put random names to the folders!
    s='c'
    for i in range(3): s+=str(choice(range(10)))
    for i in range(3): s+=chr(choice(range(97,123)))
    return s

def urls(link):
    dom=lxml.html.fromstring(urlopen(link).read())
    for l in dom.xpath('//a/@href'):
        if '#' not in l and 'jpg' in l: return l

def getimg():       # Grabbing a sequential list of 15 images
    for link in links:
        out=o+name()+'//'; mkdir(out)
        for i in range(15):
            l=link+str(i)+'/'
            print "Downloading",l,"..."
            urlretrieve(urls(l),out+str(i+1)+'.jpg')
