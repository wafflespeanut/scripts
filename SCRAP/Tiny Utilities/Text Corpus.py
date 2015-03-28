fopen = open
execfile("Download MP3s.py")
from random import shuffle

out=path.expanduser('~\Desktop\TEMP\Text Corpus\\')
link='http://www.gutenberg.org/browse/scores/top'

# Downloads the first 20 books (as text files) from the Project Gutenberg homepage
# They don't want us to download a lot of stuff in a single day (Well, they block our IPs soon). So, let's limit it to 20...

def booklist():
    s='http://www.gutenberg.org/cache/epub/'; blist=[]
    for i in set(urls(link,'ebooks')[1:]): m=i.split('/')[-1]; blist.append(s+m+'/pg'+m+'.txt')
    return shuffle(blist)[:20]

def get():
    for l in booklist(): print 'Downloading',l,'...'; urlretrieve(l,out+l.split('/')[-1])

def revise():               # A rough cleanup to Gutenberg's license & junks...
    for f in listdir(out):
        with fopen(out+f,'r') as file: data=file.readlines()
        i=0; data=data[:-362]
        while '***' not in data[i]: i+=1
        with fopen(out+f,'w') as file: file.writelines(''.join(data[i+2:]))

def scan(rmin=32,rmax=127):                # ASCII letter frequencies in range(32,127)
    freq=[0 for i in range(0,rmax)]; c=0
    for f in listdir(out):
        with fopen(out+f,'r') as file: data=file.readlines()
        for i in ''.join(data):
            m=ord(i)
            if m>=rmin and m<rmax: freq[m]+=1; c+=1
    print 'Scanned a total of %d characters from %d files!\n'%(c,len(listdir(out)))
    dfreq=dict(enumerate([float(i)/c for i in freq]))
    for k in range(len(dfreq)):
        if not dfreq[k]: del dfreq[k]
    print "Most frequently found character: '%s'"%(chr(max(dfreq.iterkeys(),key=(lambda key: dfreq[key]))))
    print "Least frequently found character: '%s'"%(chr(min(dfreq.iterkeys(),key=(lambda key: dfreq[key]))))
    print; return dfreq
