import random
import string

def sieve(n):
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i):
                sidekick[j] = False
    return [j for j,prime in enumerate(sidekick) if prime]

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
            j=0; make+=binkill(phr[i],key[j])
        i+=1; j+=1
    i=0; j=0
    while i<len(key):
        if i<len(phr): make=make[:j]+binkill(phr[j],key[i])+make[(j+1):]
        else:
            j=0; make=make[:j]+binkill(phr[j],key[i])+make[(j+1):]
        i+=1; j+=1
    return make

def hexed(key):
    pas=list(key)
    for i,j in enumerate(pas):
        pas[i]=format(ord(pas[i]),'02x')
    return pas

def char(key):
    pas=[key[i:i+2] for i in range(0,len(key),2)]
    for i,j in enumerate(pas):
        try: pas[i]=pas[i].decode("hex")
        except TypeError: return None
    return ''.join(pas)

def transpose(phr):
    punc=string.punctuation; c=False
    for i in phr:
        if i in punc:
            l=int(len(phr)**0.5); c=True
        else: l=int(len(phr)**0.5)+1
    m=0; n=len(phr)
    trans=[[0 for x in range(l)] for j in range(l)]
    mat=[phr[i:(i+l)] for i in range(m,n,m+l)]
    for i in range(len(mat)):
        while len(mat[i])<l: mat[i]+=random.choice(punc)
    for i in range(l):
        for j in range(l):
            trans[i][j]=mat[j][i]
    for i in range(l):
        trans[i]=''.join(trans[i])
    tp=''.join(trans)
    if c==True:
        while tp[-1] in punc: tp=tp[:-1]
    return tp
