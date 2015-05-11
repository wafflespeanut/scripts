# Boring stuff
i,n='','42'
while i!=n:
    a=[]; s=raw_input(); s=s.split('\n')
    for i in s:
        if i==n: break
        a.append(int(i))
    for i in a: print i
