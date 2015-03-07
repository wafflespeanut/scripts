from urllib import *
from os import mkdir
from lxml.html import *
from random import choice

o="C:\\Downloads\\"; links=[]

# I used to download comics with this...

def name():     # Just to put random names to the folders!
    return 'c'+''.join([str(choice(range(10))) for i in range(3)])+''.join([chr(choice(range(97,123))) for i in range(3)])

def title(link):
    try: p=parse(urlopen(link)); return p.find(".//title").text
    except (AttributeError,IOError): return []

def urls(link):
    tree=parse(urlopen(link))
    return [l for l in tree.xpath('//a/@href') if '#' not in l and 'html' not in l]

def getimg():       # Grabbing a sequential list of 15 images
    for link in links:
        out=o+name()+'//'; mkdir(out)
        for i in range(15):
            l=link+str(i)+'/'; print "Downloading",l,"..."
            urlretrieve(urls(l),out+str(i+1)+'.jpg')
