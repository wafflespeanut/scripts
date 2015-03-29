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
    shuffle(blist); return blist

def get():
    for l in booklist():
        if l.split('/')[-1] not in listdir(out) and l.split('/')[-1][2:] not in listdir(out):
            print 'Downloading',l,'...'; urlretrieve(l,out+l.split('/')[-1])

def revise():               # A rough cleanup of Gutenberg's license & junks...
    for f in listdir(out):
        if 'pg' in f:
            with fopen(out+f,'r') as file: data=file.readlines()
            for i,j in enumerate(data[::-1]):
                if ("End of" in j and "Project Gutenberg" in j): break
            if (len(data)-i-1)==0:
                for i,j in enumerate(data[::-1]):
                    if ("END OF" in j and "PROJECT GUTENBERG" in j): break
            data=data[:len(data)-i-1]; i=0; j=0
            while 'Produced' not in data[i] and i<30: i+=1
            while i==30 and '***' not in data[j] and j<30: j+=1
            with fopen(out+f,'w') as file: file.writelines(''.join(data[min(i,j)+4:]))
            rename(out+f,out+f[2:])

# Cleanup also requires a checkup on hand to ensure that we don't have garbage stuff

def scan(rmin=32,rmax=127):                # ASCII letter frequencies in range(32,127)
    freq=[0 for i in range(0,rmax)]; c=0
    for f in listdir(out):
        with fopen(out+f,'r') as file: data=file.readlines()
        for i in ''.join(data):
            m=ord(i)
            if m>=rmin and m<rmax: freq[m]+=1; c+=1
    print 'Scanned a total of %d characters (in the given range) from %d files!\n'%(c,len(listdir(out)))
    dfreq=dict(enumerate([float(i)/c for i in freq]))
    for k in range(len(dfreq)):
        if not dfreq[k]: del dfreq[k]
    print "Most frequently found character: '%s'"%(chr(max(dfreq.iterkeys(),key=(lambda key: dfreq[key]))))
    print "Least frequently found character: '%s'"%(chr(min(dfreq.iterkeys(),key=(lambda key: dfreq[key]))))
    print; return dfreq
