def sieve(n):
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i):
                sidekick[j] = False
    return [j for j,prime in enumerate(sidekick) if prime]
    
def hexed(key):
    pas=list(key)
    for i,j in enumerate(pas):
        pas[i]=format(ord(pas[i]),'02x')
    return pas

def char(key):
    pas=[key[i:i+2] for i in range(0,len(key),2)]
    for i,j in enumerate(pas):
        pas[i]=pas[i].decode("hex")
    return ''.join(pas)

def add(text,key):
    hand=list(''.join(text));give=list(key);num=list("0123456789");i=len(key)-1;
    for a,b in enumerate(hand):
        if i>0 and b in num:
            hand[a]=str(int(b)+ord(give[i]))[-1]
            i-=1
        elif i==0 and b in num:
            i=len(key)-1
            hand[a]=str(int(b)+ord(give[i]))[-1]
            i-=1
    return ''.join(hand)

def sub(text,key):
    hand=list(''.join(text));give=list(key);num=list("0123456789");i=len(key)-1;
    for a,b in enumerate(hand):
        if i>0 and b in num:
            hand[a]=str((10+int(b))-int(str(ord(give[i]))[-1]))[-1]
            i-=1
        elif i==0 and b in num:
            i=len(key)-1
            hand[a]=str((10+int(b))-int(str(ord(give[i]))[-1]))[-1]
            i-=1
    return ''.join(hand)

def combine(text,key):
    pas=hexed(key);phrase=hexed(text);primes=sieve(len(key)**2);
    i=0;ph=len(phrase);p=len(key)
    for j in pas:
        if primes[i]<len(phrase):
            phrase=phrase[:primes[i]]+[j]+phrase[primes[i]:]
            i+=1
        else: break
    phr=add(phrase,key)
    return ''.join(phr)

def extract(text,key):
    phrase=char(sub(text,key));primes=sieve(len(key)**2);
    ph=len(phrase);newph=""
    for i in range(ph):
        if i not in primes[:len(key)]:
            newph+=phrase[i]
    return ''.join(newph)

def eit(text,key,iteration):
    i=1;combined=combine(text,key)
    while i<=iteration:
        combined=combine(combined,key)
        i+=1
    return combined

def dit(text,key,iteration):
    i=1;extracted=extract(text,key)
    while i<=iteration:
        extracted=extract(extracted,key)
        i+=1
    return extracted

text=raw_input("Text to put in the cipher: ")
key=raw_input("Password: ")
level=raw_input("Security level (1-5, even 10 if you want!): ")

what=raw_input("Encrypt (e) or Decrypt (d) ? ")
if str(what)=='e':
    print "\n"+str(eit(str(text),str(key),int(level)))
elif str(what)=='d':
    print "\n"+str(dit(str(text),str(key),int(level)))
