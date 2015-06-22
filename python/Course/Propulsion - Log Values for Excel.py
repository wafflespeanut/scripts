import os

path = os.path.expanduser('~') + '\\Desktop\\Data\\'
out = os.path.expanduser('~') + '\\Desktop\\OUTPUT.txt'

def load(stuff):            # For grabbing specific data from a list of laboratory logs
    File = open(stuff, 'r')
    List = ''
    for i in File:
        List += i
    l = List.split('\n')
    values = []
    for i in l:
        c = 0
        for j, k in enumerate(i):
            if k == ' ' or k == '-':
                c += 1
            if c == 7:        # Values are at this position in the log file
                m = j
                t = ''
                while i[m] != ' ':
                    t += i[m]
                    m += 1
                if t != '':
                    values.append(t)
                    break
    return values

def write():
    p = os.listdir(path)
    f = []
    k = 0
    m = []
    s = [path + str(i) + os.path.splitext(p[0])[1] for i in range(len(p))]
    for i in s:
        if load(i):
            f.append(load(i))
    while k < len(f[0]):
        l = []
        for i in f:
            l.append(i[k])
        m.append(' '.join(l))
        k += 1
    t = open(out, 'w')
    t.write('\n'.join(m))
    t.close()
    return None
