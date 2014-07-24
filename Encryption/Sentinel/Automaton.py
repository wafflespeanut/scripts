def binkill(ch1,ch2):
    a=bin(ord(ch1))[2:]; b=bin(ord(ch2))[2:]; p=0; kill=""
    if len(a)>len(b): b=(len(a)-len(b))*'0'+b
    elif len(a)<len(b): a=(len(b)-len(a))*'0'+a
    while p<len(a):
        q=int(a[p])+int(b[p])
        if q==2: kill+='0'
        else: kill+=str(q)
        p+=1
    return chr(int(kill,2))

def CXOR(phr,key):
    i=0; j=0; make=""
    while i<len(phr):
        if i<len(key): make+=binkill(phr[i],key[j])
        else:
            j=0
            make+=binkill(phr[i],key[j])
        i+=1; j+=1
    i=0; j=0
    while i<len(key):
        if i<len(phr): make=make[:j]+binkill(phr[j],key[i])+make[(j+1):]
        else:
            j=0
            make=make[:j]+binkill(phr[j],key[i])+make[(j+1):]
        i+=1; j+=1
    return make
