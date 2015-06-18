from math import ceil
from os import path
from time import sleep

fin = "CTEXT-1.txt"
key = []                # Key in hex byte strings

def freq():             # Gathering data generated from a known text corpus
    fread = read('FREQ.txt')
    dfreq = {}
    for i in range(256):
        dfreq[format(i, '02x').upper()] = 0
    for i in fread:
        m = i.split('\t')
        dfreq[format(int(m[0]), '02x').upper()] = float(m[1][:-1])
    return dfreq        # Turns out that it wasn't of any use in breaking this cipher...

def read(f = fin):
    with open(f, 'r') as file:
        return file.readlines()

def write(s, f = fin):
    with open(f, 'w') as file:
        file.writelines(s)

def hexor(c1, c2):
    return int(c1, 16) ^ int(c2, 16)

def IC(ls):             # Find the index of coincidences
    data = read()
    ctext = [data[0][i:i+2] for i in range(0, len(data[0]), 2)]
    avg = 0
    for k in range(ls):
        s = [ctext[i] for i in range(k, len(ctext), ls)]
        d = {}
        for i in set(ctext):
            d[i] = s.count(i)
        ic = sum([d[i] * (d[i] - 1) for i in d]) / (float(len(s)) * (len(s) - 1))
        print 'Sequence %d (length=%d): %f' % (k + 1, len(s), ic)
        avg += ic
    return avg / ls

def analyze(rmin = 2, rmax = 13):        # Find the ICs for a range of keyspaces
    d = [0, 0]
    for k in range(rmin, rmax):
        print '\nAssuming [keyspace=%d]...\n' % (k)
        avg = IC(k)
        print '\n\tAverage IC: %f' % (avg)
        if avg > d[1]:
            d[1] = avg
            d[0] = k
    print '\nHighest IC achieved: %f (for keyspace = %d)' % (d[1], d[0])
    return d[0]

def find():                         # Find the possible plaintext suspects - This is what you should run!
    ksp = analyze()
    print '\nWaiting...'
    sleep(1.5)
    data = read()
    d = freq()
    found = []
    ctext = [data[0][i:i+2] for i in range(0, len(data[0]), 2)]
    def eng(s):
        potent = []
        for key in d:
            pi = [hexor(ci, key) for ci in s if hexor(ci, key) >= 32 and hexor(ci, key) < 127]
            if 32 in pi and len(pi) == len(s):
                potent.append((pi, key))      # Search for spaces!
        return potent
    print 'Crunching every Nth byte into sequences...'
    sleep(0.75)
    print "XOR'ing for possible values..."
    sleep(0.75)
    for seq in range(ksp):
        s = [ctext[i] for i in range(seq, len(ctext), ksp)]
        cha = [0, '']
        chose = eng(s)
        print '\n\n\tSEQUENCE', seq + 1, '- analysis results...\n\t'
        for i in chose:
            chars = sum([ch if ((ch >= 65 and ch <= 90) or (ch >= 97 and ch <= 122)) else 0 for ch in i[0]])
            # Count ASCII codes, since English chars have higher values
            print ''.join([chr(j) for j in i[0]]), '\t', i[1], '\t', chars
            if chars > cha[0]:
                cha[0] = chars
                cha[1] = i[1]
        found.append(cha[1])
    print '\n\n\tPOSSIBLE KEY:', found, '\n'

def cipher(ch):         # It deviates from the usual Vigenere in that it XORs hexed plaintext & key
    data = read()
    k = []
    if ch == 'e':
        ptext = [format(ord(i), '02x') for i in data[0]]
    elif ch == 'd':
        ptext = [data[0][i:i+2] for i in range(0, len(data[0]), 2)]
    else:
        print 'Invalid option!'
        return None
    [k.extend(key) for i in range(int(ceil(len(ptext) / float(len(key)))))]
    if ch == 'e':
        s = [format(hexor(ptext[i], k[i]), '02x') for i in range(len(ptext))]
    elif ch == 'd':
        s = [chr(hexor(ptext[i], k[i])) for i in range(len(ptext))]
    return ''.join(s)
