import random

def shift(text,shift):      # shifts the ASCII value of the chars
    try:
        new=[]; s=int(shift)
        for i,j in enumerate(text):
            m=ord(j)+shift
            while m>255: m-=255
            new+=chr(m)
    except TypeError:
        return None
    return ''.join(new)

def sieve(n):       # sieve of Eratosthenes to generate primes
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i):
                sidekick[j] = False
    return [j for j,prime in enumerate(sidekick) if prime]

def hexed(key):     # hexing function
    pas=list(key)
    for i,j in enumerate(pas):
        pas[i]=format(ord(pas[i]),'02x')
    return pas

def char(key):      # hex-decoding function
    pas=[key[i:i+2] for i in range(0,len(key),2)]
    for i,j in enumerate(pas):
        try:
            pas[i]=pas[i].decode("hex")
        except TypeError:
            return None
    return ''.join(pas)

def add(text,key):      # adds the ASCII values of key and phrase chars
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

def sub(text,key):      # gets the key and phrase chars back!
    hand=list(''.join(text)); give=list(key);
    num=list("0123456789"); i=len(key)-1
    for a,b in enumerate(hand):     # executes from the last char
        if i>0 and b in num:
            hand[a]=str((10+int(b))-int(str(ord(give[i]))[-1]))[-1]
            i-=1
        elif i==0 and b in num:
            i=len(key)-1
            hand[a]=str((10+int(b))-int(str(ord(give[i]))[-1]))[-1]
            i-=1
    return ''.join(hand)

def primelist(level):       #throws the primes wanted for randomgen
    k=2**(5+level)
    return sieve(k*k)

def keypnum(key,level):       # generates primes based on the key-chars' ASCII values
    primes=[]; plist=primelist(level/2)
    for i in key:
        primes+=[str(plist[ord(i)])]
    for n in range(level):
        temp=[]; temp+=''.join(primes)
        for i,j in enumerate(temp):
            primes+=[str(plist[int(j)])]
    return ''.join(primes)

def pop(key,level):       # confuses & constrains the sliced list to 8-chars
    merged=[]; p=keypnum(key,level)
    while len(p)>=8:
        merged.append(p[0:8])
        p=p[8:]
    return list(set(merged))

def find(text,key,level):     # finds the random key used during encryption
    listed=pop(key,level)
    for i,j in enumerate(listed):
        rkey=combine(j,key)
        if extract(extract(text,rkey),key)!=None:
            return extract(text,rkey)
        else: continue
    return None

def combine(text,key):      # dissolves key chars into the phrase
    try:
        pas=hexed(key); phrase=hexed(text)
        primes=sieve(len(key)**2)
        i=0; ph=len(phrase);
        for j in pas:
            if primes[i]<len(phrase):
                phrase=phrase[:primes[i]]+[j]+phrase[primes[i]:]
                i+=1
            else: break
    except IndexError:
        return None
    phr=add(phrase,key)
    return ''.join(phr)

def extract(text,key):      # removes the key chars from the phrase
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

def eit(text,key,iteration):        # iteration, shifting, random key, etc.
    i=1; combined=combine(text,key)
    p=pop(key,iteration); random.shuffle(p)
    rkey=combine(random.choice(p),key)
    while i<iteration:
        combined=combine(combined,key)
        i+=1
    combined=combine(combined,rkey)
    if combined==None:
        return None
    zombie=combined
    for i in key:
        zombie=shift(zombie,ord(i))
    return ''.join(hexed(add(zombie,key)))

def dit(text,key,iteration):        # the whole eit() thing in reverse...
    zombie=sub(char(text),key)
    for i in key:
        zombie=shift(zombie,255-ord(i))
    i=1; extracted=find(zombie,key,iteration)
    while i<=iteration:
        extracted=extract(extracted,key)
        i+=1
    if extracted==None:
        return None
    return extracted

def zombify():      # user interface
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
            while str(level) not in "012345":
                print "\n Enter a number ranging from 1-5\n"
                level=raw_input("Security level (1-5): ")
            if str(level)=="":
                print "\n No input given. Choosing level 1\n"
                level=1
            what=raw_input("Encrypt (e) or Decrypt (d) ? ")
            while str(what)!="e" and str(what)!="d" and str(what)=="":
                print "\n (sigh) You can choose something...\n"
                what=raw_input("Encrypt (e) or Decrypt (d) ? ")
            if str(what)=='e':
                out=eit(str(text),str(key),int(level))
                print "\n"+str(out)+"\n"
            elif str(what)=='d': # While decrypting, (given the correct key) a lower iteration level can decrypt the data, but it can't get back to the message!
                out=dit(str(text),str(key),int(level))
                if out==None:
                    print "\n Mismatch between ciphertext and key!!!\n\nPossibly due to:\n\t- Incorrect key (Check your password!)\n\t- Varied iterations (Check your security level!)\n\t(or) such an exotic ciphertext doesn't even exist!!! (Testing me?)\n"
                else: print "\nMESSAGE: "+str(out)+"\n"
            choice=raw_input("Do something again: (y/n)? ")
    except KeyboardInterrupt:
        return None
