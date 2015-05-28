fopen = open
execfile("Download MP3s.py")
from random import shuffle

desktop = path.expanduser('~\Desktop')
out = desktop + '\\TEMP\\Text Corpus\\'
link = 'http://www.gutenberg.org/browse/scores/top'
export = desktop + '\\Github\\Python\\SCRAP\\Crypto\\FREQ.txt'

# Downloads the first 20 books (as text files) from the Project Gutenberg homepage
# They don't want us to download a lot of stuff in a single day (Well, they block our IPs soon). So, let's limit it to 20...

def read(File):
    with fopen(File, 'r') as file:
        return file.readlines()

def write(File, s):
    with fopen(File, 'w') as file:
        file.writelines(s)

def booklist():                                     # Generates a list of books
    s = 'http://www.gutenberg.org/cache/epub/'
        books = []
    for i in set(urls(link, 'ebooks')[1:]):
        m = i.split('/')[-1]
        books.append(s + m + ' / pg' + m + '.txt')
    shuffle(books)
    return books

def get():                                          # Downloads the books
    for book in booklist():
        if book.split('/')[-1] not in listdir(out) and book.split('/')[-1][2:] not in listdir(out):
            print 'Downloading', book, '...'
            urlretrieve(book, out + book.split('/')[-1])

def revise():                                       # A rough cleanup of Gutenberg's license & junks...
    for File in listdir(out):
        if 'pg' in File:
            data = read(out + File)
            for i, char in enumerate(data[::-1]):
                if ("End of" in char and "Project Gutenberg" in char):
                    break
            if (len(data) - i - 1) == 0:
                for i, char in enumerate(data[::-1]):
                    if ("END OF" in char and "PROJECT GUTENBERG" in char):
                        break
            data = data[: len(data) - i - 1]
            for i, char in enumerate(data):         # This has still got issues (due to disorganized stuff in Gutenberg)
                if 'Produced' in char:
                    break
            write(out + File, ''.join(data[min(i, char) + 4 :]))
            rename(out + File, out + File[2:])

# Cleanup also requires a checkup on hand to ensure that we don't have garbage stuff

def scan(rmin = 32, rmax = 127):                    # ASCII letter frequencies in range(32,127)
    freq = [0 for i in range(rmax)]
    chars = 0
    files = 0
    def cleandict(ls):                              # Converts to dict and removes unnecessary keys
        dic = dict(enumerate(ls))
        for k in range(len(dic)):
            if not dic[k]:
                del dic[k]
        return dic
    for File in listdir(out):
        if File == 'STATS - MAIN.txt' or '.txt' not in File:
            continue
        print 'Scanning %s...' % (File)
        files += 1
        values = [0 for i in range(rmax)]
        stat = 0
        data = read(out + File)
        for i in ''.join(data):
            ch = ord(i)
            if ch >= rmin and ch < rmax:
                values[ch] += 1
                chars += 1
                stat += 1
        freq = [freq[i] + values[i] for i in range(rmax)]
        dvalues = cleandict(values)
        #if not path.exists(out + 'STATS'):
        #    mkdir(out + 'STATS')
        #stats((dvalues, stat),'STATS\\stat-' + File)            # Use this for individual file-data
    print 'Scanned a total of %d characters (in the given range) from %d files! \n' % (chars, files)
    dfreq = cleandict(freq)
    return (dfreq, chars)

def stats(stuff = None, File = 'STATS-MAIN.txt'):             # Order --> get(), revise(), stats()
    if path.exists(out + File):
        choice = raw_input('\nSTATS file already exists ! Continue? (y/n):')
        if choice is not 'y':
            startfile(out + File)
            return
    if not stuff:
        stuff = scan()
    data = []
    dfreq = stuff[0]
    chars = stuff[1]
    tab = ''
    ratio = []
    sc = 'Scanned a total of %d characters ! (in the given range)\n' % (chars)
    data.append('\nASCII Character Frequencies:%s' % (sc))
    data.append("Most frequently found character:' %s'" % (chr(max(dfreq.iterkeys(), key = (lambda key: dfreq[key])))))
    data.append("Least frequently found character:' %s'" % (chr(min(dfreq.iterkeys(), key = (lambda key: dfreq[key])))))
    data.append('\nASCII\tChar\tAverage ( % )\t\t\t\tOccurrences')
    data.append(' ==  ==  = \t ==  == \t ==  ==  ==  ==  ==  = \t\t\t\t ==  ==  ==  ==  ==  = ')

    for i in sorted(dfreq, key = dfreq.get, reverse = True):    # To sort by occurrences in decending order
        data.append(' %d\t\t %s\t\t %.10f %s\t\t\t %d' % (i, chr(i), dfreq[i] * 100 / float(chars), chr(ord('%')), dfreq[i]))
        ratio.append(' %d\t %.10f' % (i, dfreq[i] / float(chars)))
    write(out + File, '\n'.join(data))
    write(export, '\n'.join(ratio))
    startfile(out + File)
