def life(n):
    i=''
    while i!=str(n):
        a=[]
        s=raw_input(); s=s.split('\n')
        for i in s:
            if i==str(n): break
            a.append(int(i))
        for i in a: print i
