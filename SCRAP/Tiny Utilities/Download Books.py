execfile("Download MP3s.py")
from os import *

out="C:\\Users\\Waffles Crazy Peanut\\Desktop\\TEMP\\Text Corpus\\"
link='http://www.gutenberg.org/browse/scores/top'

# Downloads the first 20 books (as text files) from the Project Gutenberg homepage
# They don't want us to download a lot of stuff in a single day (Well, they block our IPs soon). So, let's limit it to 20...

def booklist():
    s='http://www.gutenberg.org/cache/epub/'; blist=[]
    for i in set(urls(link,'ebooks')[1:]): m=i.split('/')[-1]; blist.append(s+m+'/pg'+m+'.txt')
    return blist[:20]

def get():
    for l in booklist(): print 'Downloading',l,'...'; urlretrieve(l,out+l.split('/')[-1])

def arrange():
    for i in listdir(out):
        
