import random, timeit

def sieve(n):
    '''Generates a list of primes using the sieve of Eratosthenes'''
    sidekick=[False]*2+[True]*(n-1)
    for i in range(int(n**0.5)+1):
        if sidekick[i]:
            for j in range(i*i,n+1,i): sidekick[j]=False
    return [j for j,p in enumerate(sidekick) if p]

def CXOR(phr,key): # quite useful for XOR'ing bulk text & key (reversible)
    def xor(ch1,ch2): # XOR's two chars
        a=ord(ch1); b=ord(ch2)
        return chr(a^b)
    i=0; j=0; make=""
    while i<len(phr):
        if i<len(key): make+=xor(phr[i],key[j])
        else: j=0; make+=xor(phr[i],key[j])
        i+=1; j+=1
    i=0; j=0
    while i<len(key):
        if i<len(phr): make=make[:j]+xor(phr[j],key[i])+make[(j+1):]
        else: j=0; make=make[:j]+xor(phr[j],key[i])+make[(j+1):]
        i+=1; j+=1
    return make

def hexed(key): # hexing function
    pas=list(key)
    for i,j in enumerate(pas): pas[i]=format(ord(pas[i]),'02x')
    return pas

def add(text,key): # adds the ASCII values of key and phrase chars
    hand=list(''.join(text));give=list(key);
    num=list("0123456789"); i=len(key)-1
    for a,b in enumerate(hand):
        if i>0 and b in num: hand[a]=str(int(b)+ord(give[i]))[-1]; i-=1
        elif i==0 and b in num: i=len(key)-1; hand[a]=str(int(b)+ord(give[i]))[-1]; i-=1
    return ''.join(hand)

def keypnum(key,level): # generates primes based on the key-chars' ASCII values
    def primelist(level): # throws the primes wanted for randomgen
        k=2**(5+level); return sieve(k*k)
    primes=[]; plist=primelist(level/2)
    for i in key: primes+=[str(plist[ord(i)])]
    for n in range(level):
        temp=[]; temp+=''.join(primes)
        for i,j in enumerate(temp): primes+=[str(plist[int(j)])]
    return ''.join(primes)

def pop(key,level): # confuses & constrains the sliced list to 8-chars
    merged=[]; p=keypnum(key,level)
    while len(p)>=8: merged.append(p[0:8]); p=p[8:]
    return list(set(merged))

def combine(text,key): # dissolves key chars into the phrase
    try:
        phrase=hexed(text); phr=add(phrase,key)
    except IndexError: return None
    return ''.join(phr)

def char(key): # hex-decoding function
    pas=[key[i:i+2] for i in range(0,len(key),2)]
    for i,j in enumerate(pas):
        try: pas[i]=pas[i].decode("hex")
        except TypeError: return None
    return ''.join(pas)

def sub(text,key): # gets the key and phrase chars back!
    try:
        hand=list(''.join(text)); give=list(key); num=list("0123456789"); i=len(key)-1
        for a,b in enumerate(hand): # executes from the last char
            if i>0 and b in num:
                hand[a]=str((10+int(b))-int(str(ord(give[i]))[-1]))[-1]; i-=1
            elif i==0 and b in num:
                i=len(key)-1
                hand[a]=str((10+int(b))-int(str(ord(give[i]))[-1]))[-1]; i-=1
        out=''.join(hand)
    except TypeError: return None
    return out

def find(text,key,level): # finds the random key used during encryption
    listed=pop(key,level)
    for i,j in enumerate(listed):
        rkey=combine(j,key)
        if extract(extract(text,rkey),key)!=None: return extract(text,rkey)
        else: continue
    return None

def extract(text,key): # removes the key chars from the phrase
    try:
        phrase=''.join(char(sub(text,key)))
    except TypeError: return None
    return phrase

def shift(text,shift): # shifts the ASCII value of the chars (reversible)
    try:
        new=[]; s=int(shift)
        for i,j in enumerate(text):
            m=ord(j)+shift
            while m>255: m-=255
            new+=chr(m)
    except TypeError: return None
    return ''.join(new)

def eit(text,key,iteration): # iteration, shifting, random key, etc.
    i=1; start=timeit.default_timer()
    combined=combine(text,key)
    stop=timeit.default_timer()
    print "> Adding Binary, ASCII, Hexing... " +str(round(stop-start,5)) +" seconds"
    start=timeit.default_timer()
    p=pop(key,iteration); random.shuffle(p); rkey=combine(random.choice(p),key)
    stop=timeit.default_timer()
    print "> Generating random key... " +str(round(stop-start,5)) +" seconds"
    if i<iteration:
        start=timeit.default_timer()
        while i<iteration: combined=combine(combined,key); i+=1
        stop=timeit.default_timer()
        print "> Iterating... " +str(round(stop-start,5)) +" seconds"
    start=timeit.default_timer()
    combined=combine(combined,rkey)
    stop=timeit.default_timer()
    print "> Using random key... " +str(round(stop-start,5)) +" seconds"
    if combined==None: return None
    start=timeit.default_timer()
    zombie=combined; pas=''.join(hexed(key))
    for i in key: zombie=shift(zombie,ord(i))
    out=add(zombie,key); xor=CXOR(out,pas)
    stop=timeit.default_timer()
    print "> Shifting, Adding ASCII values, XOR'ing... " +str(round(stop-start,5)) +" seconds"
    return ''.join(hexed(xor))

def dit(text,key,iteration): # the whole eit() thing in reverse...
    start=timeit.default_timer()
    pas=''.join(hexed(key)); xor=CXOR(char(text),pas); zombie=sub(xor,key)
    for i in key:
        zombie=shift(zombie,255-ord(i))
    stop=timeit.default_timer()
    print "> XOR'ing, Shifting, Getting back ASCII values... " +str(round(stop-start,5)) +" seconds"
    i=1; start=timeit.default_timer()
    extracted=find(zombie,key,iteration)
    stop=timeit.default_timer()
    print "> Finding the random key... " +str(round(stop-start,5)) +" seconds"
    start=timeit.default_timer()
    while i<iteration: extracted=extract(extracted,key); i+=1
    stop=timeit.default_timer()
    print "> Reverse iterating... " +str(round(stop-start,5)) +" seconds"
    start=timeit.default_timer()
    extracted=extract(extracted,key)
    stop=timeit.default_timer()
    print "> Decoding hex & Getting back ASCII values... " +str(round(stop-start,5)) +" seconds"
    if extracted==None: return None
    return extracted

def zombify(what,text,key,level):
    if what=='e':
        print "\nENCRYPTING...\n"
        out=eit(text,key,int(level))
        return str(out)
    elif what=='d':
        print "\nDECRYPTING...\n"
        out=dit(text,key,int(level))
        if out==None: return None
        else: return str(out)

def RUN():      # User Interface
    try:
        choice='y'
        while choice=='y':
            text=str(raw_input("\nText to put in the cipher: "))
            while text=="":
                print "\n Um, I don't see any text here... Gimme something to eat!!!"
                text=str(raw_input("\nText to be encrypted: "))
            key=str(raw_input("Password: "))
            while len(key)==1 or str(key)=="":
                if key=="":
                    print "\n No password? You do want me to encrypt, right?\n"
                    key=str(raw_input("What's the password? "))
                elif len(key)==1:
                    print "\n No, Seriously? Password of unit length? Try something bigger...\n"
                    key=str(raw_input("Choose a password: "))
            level=str(raw_input("Security level (1-5, for fast output): "))
            while level=='' or ord(level) not in range(49,54):
                print "\n Enter a number ranging from 1-5!\n"
                level=raw_input("Security level (1-5): ")
            what=str(raw_input("Encrypt (e) or Decrypt (d) ? "))
            while what!="e" and what!="d":
                print "\n (sigh) You can choose something...\n"
                what=str(raw_input("Encrypt (e) or Decrypt (d) ? "))
            start=timeit.default_timer()
            s=zombify(what,text,key,level)
            stop=timeit.default_timer()
            if s==None: print "\n Mismatch between ciphertext and key!!!\n\nPossibly due to:\n\t- Incorrect key (Check your password!)\n\t- Varied iterations (Check your security level!)\n\t(or) such an exotic ciphertext doesn't even exist!!! (Testing me?)\n"
            else: print "\nTOTAL TIME:",round(stop-start,5),"seconds"; print '\nMESSAGE: %s\n'%(s)
            choice=str(raw_input("Do something again: (y/n)? "))
    except KeyboardInterrupt: return None

def FILE():     # Encrypts/Decrypts files
    try:
        i=0; key=str(raw_input("Password: "))
        while len(key)==1 or str(key)=="":
            if key=="":
                print "\n No password? You do want me to encrypt, right?\n"
                key=str(raw_input("What's the password? "))
            elif len(key)==1:
                print "\n No, Seriously? Password of unit length? Try something bigger...\n"
                key=str(raw_input("Choose a password: "))
        level=str(raw_input("Security level (1-5, for fast output): "))
        while level=='' or ord(level) not in range(49,54):
            print "\n Enter a number ranging from 1-5!\n"
            level=raw_input("Security level (1-5): ")
        what=str(raw_input("Encrypt (e) or Decrypt (d) ? "))
        while what!="e" and what!="d":
            print "\n (sigh) You can choose something...\n"
            what=str(raw_input("Encrypt (e) or Decrypt (d) ? "))
        while True:
            path=str(raw_input("Enter File name (including path): "))
            try: File=open(path,'r'); File.close(); break
            except IOError: print "\n INVALID PATH!\n"
        start=timeit.default_timer()
        with open(path,'r') as file: data=file.readlines()
        while i<len(data):
            data[i]=zombify(what,str(data[i][:-1]),key,level)
            if data[i]==None: print "\n Mismatch between ciphertext and key!!!\n\nPossibly due to:\n\t- Incorrect key (Check your password!)\n\t- Varied iterations (Check your security level!)\n\t(or) such an exotic ciphertext doesn't even exist!!! (Testing me?)\n"; break
            data[i]+='\n'; i+=1
        with open(path,'w') as file: file.writelines(data)
        stop=timeit.default_timer()
        print "\nTOTAL TIME:",round(stop-start,5),"seconds"
    except KeyboardInterrupt: return None
