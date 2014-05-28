import random

def shift(text,shift):
    try:
        new=[]; s=int(shift)
        for i,j in enumerate(text):
            m=ord(j)+shift
            while m>255: m-=255
            new+=chr(m)
    except TypeError:
        return None
    return ''.join(new)

def sieve(n):
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i):
                sidekick[j] = False
    return [j for j,prime in enumerate(sidekick) if prime]

primelist=sieve(512**2)

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
    hand=list(''.join(text));give=list(key);
    num=list("0123456789"); i=len(key)-1
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
    hand=list(''.join(text)); give=list(key);
    num=list("0123456789"); i=len(key)-1
    for a,b in enumerate(hand):
        if i>0 and b in num:
            hand[a]=str((10+int(b))-int(str(ord(give[i]))[-1]))[-1]
            i-=1
        elif i==0 and b in num:
            i=len(key)-1
            hand[a]=str((10+int(b))-int(str(ord(give[i]))[-1]))[-1]
            i-=1
    return ''.join(hand)

def keypnum(key):
    primes=[]
    for i in key:
        for j in range(1,3):
            primes+=[str(primelist[ord(i)]**(j+1))]
    return primes

def slicing(key):
    listed=[]; sliced=[]; l=10
    for i in key:
        listed+=[int(i)]
    for i,j in enumerate(listed):
        k=0
        while len(str(listed[i]))<l:
            listed[i]+=listed[k]
            k+=1
            if k==len(key): k=0
        while len(str(listed[i]))>l:
            listed[i]-=listed[k]
            k+=1
            if k==len(key): k=0
    for p in listed:
        sliced+=[str(p)]
    return sliced

def pop(key):
    listed=keypnum(key)
    listed.extend(keypnum(''.join(listed)))
    return slicing(list(set(listed)))

def find(text,key):
    listed=pop(key)
    for i,j in enumerate(listed):
        if extract(extract(text,j),key)!=None:
            return extract(text,j)
        else: continue
    return None

def combine(text,key):
    try:
        pas=hexed(key); phrase=hexed(text);
        primes=sieve(len(key)**2)
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
        phrase=char(sub(text,key));
        primes=sieve(len(key)**2)
        ph=len(phrase); newph=""
        for i in range(ph):
            if i not in primes[:len(key)]:
                newph+=phrase[i]
    except TypeError:
            return None
    return ''.join(newph)

def eit(text,key,iteration):
    i=1; combined=combine(text,key);
    p=pop(key); random.shuffle(p)
    while i<iteration:
        combined=combine(combined,key)
        i+=1
    if i==iteration or iteration==0:
        random.shuffle(p)
        combined=combine(combined, random.choice(p))
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
    i=1; extracted=find(zombie,key)
    if iteration==0:
        extracted=extract(extracted,key)
    while i<iteration:
        extracted=extract(extracted,key)
        i+=1
    if i==iteration:
        extracted=extract(extracted,key)
    if extracted==None:
        return None
    return extracted

def zombify():
    try:
        choice='y'
        while choice=='y':
            text=raw_input("\nText to put in the cipher: ")
            while str(text)=="":
                print "\n Um, I don't see any text here... Gimme something to eat!!!"
                text=raw_input("\nText to be encrypted: ")
            key=raw_input("Password: ")
            while len(str(key))==1 or str(key)=="":
                if str(key)=="":
                    print "\n No password? You do want me to encrypt, right?\n"
                    key=raw_input("What's the password? : ")
                elif len(str(key))==1:
                    print "\n No, Seriously? Password of unit length? Try something better...\n"
                    key=raw_input("Choose a password: ")
            level=raw_input("Security level (1-5, for fast output): ")
            while str(level) not in "12345":
                print "\n Enter a number ranging from 1-5\n"
                level=raw_input("Security level (1-5): ")
            if str(level)=="":
                print "\n No input given. Choosing level 1\n"
                level=0
            what=raw_input("Encrypt (e) or Decrypt (d) ? ")
            while str(what)!="e" and str(what)!="d" and str(what)=="":
                print "\n (sigh) You can choose something...\n"
                what=raw_input("Encrypt (e) or Decrypt (d) ? ")
            if str(what)=='e':
                out=eit(str(text),str(key),int(level))
                print "\n"+str(out)+"\n"
            elif str(what)=='d':
                out=dit(str(text),str(key),int(level))
                if out==None:
                    print "\n Mismatch between ciphertext and key!!!\n\nPossibly due to:\n\t- Incorrect key (Check your password!)\n\t- Varied iterations (Check your security level!)\n\t(or) such an exotic ciphertext doesn't even exist!!! (Testing me?)\n"
                else: print "\nMESSAGE: "+str(out)+"\n"
            choice=raw_input("Do something again: (y/n)? ")
    except KeyboardInterrupt:
        return None

zombify()
