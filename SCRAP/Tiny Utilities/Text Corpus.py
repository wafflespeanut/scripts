fopen = open
execfile("Download MP3s.py")
from random import shuffle

desk=path.expanduser('~\Desktop'); out=desk+'\\TEMP\\Text Corpus\\'
link='http://www.gutenberg.org/browse/scores/top'
export=desk+'\\Github\\Python\\SCRAP\\Crypto\\FREQ.txt'

# Downloads the first 20 books (as text files) from the Project Gutenberg homepage
# They don't want us to download a lot of stuff in a single day (Well, they block our IPs soon). So, let's limit it to 20...

def read(f):
    with fopen(f,'r') as file: return file.readlines()

def write(loc,s):
    with fopen(loc,'w') as file: file.writelines(s)

def booklist():             # Generates a list of books
    s='http://www.gutenberg.org/cache/epub/'; blist=[]
    for i in set(urls(link,'ebooks')[1:]): m=i.split('/')[-1]; blist.append(s+m+'/pg'+m+'.txt')
    shuffle(blist); return blist

def get():                  # Downloads the books
    for l in booklist():
        if l.split('/')[-1] not in listdir(out) and l.split('/')[-1][2:] not in listdir(out):
            print 'Downloading',l,'...'; urlretrieve(l,out+l.split('/')[-1])

def revise():               # A rough cleanup of Gutenberg's license & junks...
    for f in listdir(out):
        if 'pg' in f:
            data=read(out+f)
            for i,j in enumerate(data[::-1]):
                if ("End of" in j and "Project Gutenberg" in j): break
            if (len(data)-i-1)==0:
                for i,j in enumerate(data[::-1]):
                    if ("END OF" in j and "PROJECT GUTENBERG" in j): break
            data=data[:len(data)-i-1]; i=0; j=0
            while 'Produced' not in data[i] and i<30: i+=1
            while i==30 and '***' not in data[j] and j<30: j+=1
            write(out+f,''.join(data[min(i,j)+4:]))
            rename(out+f,out+f[2:])

# Cleanup also requires a checkup on hand to ensure that we don't have garbage stuff

def scan(rmin=32,rmax=127):                # ASCII letter frequencies in range(32,127)
    freq=[0 for i in range(rmax)]; c=0; z=0
    def cleandict(ls):                      # Converts to dict and removes unnecessary keys
        dic=dict(enumerate(ls))
        for k in range(len(dic)):
            if not dic[k]: del dic[k]
        return dic
    for f in listdir(out):
        if f=='STATS-MAIN.txt' or '.txt' not in f: continue
        print 'Scanning %s...'%(f); z+=1
        temp=[0 for i in range(rmax)]; ct=0; data=read(out+f)
        for i in ''.join(data):
            m=ord(i)
            if m>=rmin and m<rmax: temp[m]+=1; c+=1; ct+=1
        freq=[freq[i]+temp[i] for i in range(rmax)]; dtemp=cleandict(temp)
        #if not path.exists(out+'STATS'): mkdir(out+'STATS')
        #stats((dtemp,ct),'STATS\\stat-'+f)                     # Use this for individual file data
    print 'Scanned a total of %d characters (in the given range) from %d files!\n'%(c,z)
    dfreq=cleandict(freq)
    return (dfreq,c)

def stats(stuff=None,F='STATS-MAIN.txt'):
    if path.exists(out+F):
        s=raw_input('\nSTATS file already exists! Continue? (y/n): ')
        if s!='y': startfile(out+F); return
    if not stuff: stuff=scan()
    w=[]; dfreq=stuff[0]; c=stuff[1]; tab=''; z=[]
    sc='Scanned a total of %d characters! (in the given range)\n'%(c)
    w.append('\nASCII Character Frequencies: %s'%(sc))
    w.append("Most frequently found character: '%s'"%(chr(max(dfreq.iterkeys(),key=(lambda key: dfreq[key])))))
    w.append("Least frequently found character: '%s'"%(chr(min(dfreq.iterkeys(),key=(lambda key: dfreq[key])))))
    w.append('\nASCII\tChar\tOccurrences\t\t(in percent)')
    w.append('=====\t====\t===========\t\t============')
    for i in sorted(dfreq,key=dfreq.get,reverse=True):          # To sort by occurrences in decending order
        if len(str(dfreq[i]))>=4: tab='\t\t\t'
        else: tab='\t\t\t\t'
        w.append('%d\t\t%s\t\t%d%s%.10f %s'%(i,chr(i),dfreq[i],tab,dfreq[i]*100/float(c),chr(ord('%'))))
        z.append('%d\t%.10f'%(i,dfreq[i]/float(c)))
    write(out+F,'\n'.join(w)); write(export,'\n'.join(z))
    startfile(out+F)
