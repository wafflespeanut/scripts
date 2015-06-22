execfile("Variant Vigenere.py")
from math import ceil
from os import path
from time import sleep

fin = "CTEXT-2.txt"
# Key in hex byte strings
key = ['00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00']
# That's how you start!

# key = ['F2', '1A', '04', '9B', 'D0', '73', '23', 'C8', '39', '98', 'CE', '09', '0E', 'BC', '86', 'DA', 'C9', 'E0', '39', '89', '2A', '5F', '72', '67', '83', 'A5', '61', 'FD', '25', 'EE', '30']
# Key obtained by repetitive ctext(n) and test() - Boring!

def check(c1, c2):       # XOR stuff and return possible values (eliminating spaces)
    if not len(c1) == len(c2):
        return None
    alp = []
    t1 = [c1[i:i+2] for i in range(0, len(c1), 2)]
    t2 = [c2[i:i+2] for i in range(0, len(c2), 2)]
    for i in range(len(t1)):
        p = str(hexor(t1[i], t2[i]))
        s = (' ' + p if len(p) < 2 else p)
        alp.append(' ' + chr(32 ^ int(s)) if 32 ^ int(s) in range(65, 122) else '  ')
    return alp

def ctext(m):           # Rough way to guess the keys
    with open(fin, 'r') as file:
        data = file.readlines()
    data = [i[:-1] if i[-1] == '\n' else i for i in data]
    k = key
    r = (' ' + str(i) if i / 10 == 0 else str(i) for i in range(len(data[m - 1]) / 2))
    print '  '.join(r), '\n'
    collect = data[m - 1]
    for i in range(len(data)):
        alp = check(data[m - 1], data[i])
        if m == (i + 1):
            continue
        print '  '.join(alp), ' ', (m, i + 1)
    while True:
        try:
            p = int(raw_input('\nPosition: '))
            ch = raw_input('Possible character: ')
            try:
                ch = format(ord(ch), '02x')           # In case we insert an additional space
            except TypeError:
                ch = format(ord(ch.split(' ')[-1]), '02x')
            l = collect[p]
            k[p] = format(hexor(l, ch), '02x').upper()
        except (KeyboardInterrupt, ValueError):
            print 'Testing new key...\n'
            test(k)
            return k

def test(k = key):        # To manually test whether it's readable English - This is what you should run!
    with open(fin, 'r') as file:
        data = file.readlines()
    data = [i[:-1] if i[-1] == '\n' else i for i in data]
    r = (' ' + str(i) if i / 10 == 0 else str(i) for i in range(len(k)))
    print '  '.join(r), '\n'
    for b, c in enumerate(data):
        s = []
        ch = [c[i:i+2] for i in range(0, len(c), 2)]
        for i in range(len(ch)):
            m = hexor(ch[i], k[i])
            s.append(' ' + chr(m))
        print '  '.join(s), '\t', [b + 1]
