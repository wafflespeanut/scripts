def shift(text,shift):
    new=[]; s=int(shift)
    for i,j in enumerate(text):
        m=ord(j)+shift
        while m>255: m-=255
        new+=chr(m)
    return ''.join(new)

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
        try:
            pas[i]=pas[i].decode("hex")
        except TypeError:
            return None
    return ''.join(pas)

def add(text,key):
    hand=list(''.join(text));give=list(key); num=list("0123456789"); i=len(key)-1
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
    hand=list(''.join(text)); give=list(key); num=list("0123456789"); i=len(key)-1
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
    try:
        pas=hexed(key); phrase=hexed(text); primes=sieve(len(key)**2)
        i=0; ph=len(phrase); p=len(key)
        for j in pas:
            if primes[i]<len(phrase):
                phrase=phrase[:primes[i]]+[j]+phrase[primes[i]:]
                i+=1
            else: break
    except IndexError:
        return None
    phr=add(phrase,key)
    return ''.join(phr)

def extract(text,key):
    try:
        phrase=char(sub(text,key)); primes=sieve(len(key)**2)
        ph=len(phrase); newph=""
        for i in range(ph):
            if i not in primes[:len(key)]:
                newph+=phrase[i]
    except TypeError:
            return None
    return ''.join(newph)

def eit(text,key,iteration):
    i=1; combined=combine(text,key);
    while i<=iteration:
        combined=combine(combined,key)
        i+=1
    if combined==None:
        return None
    zombie=combined
    for i in key:
        zombie=shift(zombie,ord(i))
    return ''.join(hexed(zombie))

def dit(text,key,iteration):
    zombie=char(text)
    for i in key:
        zombie=shift(zombie,255-ord(i))
    i=1; extracted=extract(zombie,key)
    while i<=iteration:
        extracted=extract(extracted,key)
        i+=1
    if extracted==None:
        return None
    return extracted

def zombify():
    choice='y'
    while choice=='y':
        text=raw_input("\nText to put in the cipher: ")
        key=raw_input("Password: ")
        while len(str(key))==1:
            print "\n No, Seriously? Password of unit length? Try something better...\n"
            key=raw_input("Password: ")
        level=raw_input("Security level (1-5, for fast output): ")
        while str(level) not in "0123456789":
            print "\n Enter a number ranging from 0-9\n"
            level=raw_input("Security level (1-5, for fast output): ")
        what=raw_input("Encrypt (e) or Decrypt (d) ? ")
        if str(what)=='e':
            out=eit(str(text),str(key),int(level))
            print "\n"+str(out)+"\n"
        elif str(what)=='d':
            out=dit(str(text),str(key),int(level))
            if out==None:
                print "\n Mismatch between ciphertext and key!!!\n\nPossibly due to:\n\t- Incorrect key (Check your password!)\n\t- Varied iterations (Check your security level!)\n\t(or) such an exotic ciphertext doesn't even exist!!! (Testing me?)\n"
            else: print "\nMESSAGE: "+str(out)+"\n"
        else: print "\n Illegal choice!!!\n"
        choice=raw_input("Do something again: (y/n)? ")

zombify()
