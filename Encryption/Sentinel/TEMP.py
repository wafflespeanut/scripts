def group(text):
    dupe=''.join(set(text)); availed=""
    for i in dupe:
        availed+=i
        for j in text:
            if j==i: availed+='1'
            else: availed+='0'
        availed+='|'
    ph=availed[:(len(availed)-1)]
    li=ph.split('|')
    for i in range(len(li)):
        while li[i][-1]!='1':
            li[i]=li[i][:-1]
    return '|'.join(li)

def binshield(text,key): # adds punctuation to the text
    ph=group(text); i=0; k=0; punc='!"#$%&\'()*+,-./';
    while k<len(ph):
        if ph[k]=='0':
            c=0
            while ph[k+c]=='0':
                c+=1
                if k+c >= len(ph): break
            if(c>2): ph=ph[:k]+random.choice(punc)+str(c)+random.choice(punc)+ph[(c+k):]
        k+=1
    i=0; punc=':;<=>?@[\\]^_`{}~'
    while i<len(ph):
        if ph[i]=='1':
            c=0
            while ph[i+c] in '01':
                c+=1
                if i+c >= len(ph): break
            if c>1: ph=ph[:i]+random.choice(punc)+str(int(ph[i:(i+c)],2))+random.choice(punc)+ph[(c+i):]
        i+=1
    return ph

def remshield(text): # removes the random punctuations
    punc=':;<=>?@[\\]^_`{}~'; ph=""; i=0; num='0123456789'
    while i<len(text):
        if text[i] not in punc:
            ph+=text[i]
        else:
            c=i+1
            while text[c] in num:
                c+=1
            if text[i+1] in num:
                ph+=bin(int(text[(i+1):c]))[2:]
                i+=(c-i)
        i+=1
    text=ph; ph=""; punc='!"#$%&\'()*+,-./'; i=0
    while i<len(text):
        if text[i] not in punc:
            ph+=text[i]
        elif text[i]=='|':
            ph+=text[i]
            i+=2
        else:
            c=i+1
            while text[c] in num:
                c+=1
            if text[i+1] in num:
                ph+=int(text[(i+1):c])*'0'
                i+=(c-i)
        i+=1
    return ph

def pick(text,char): # a function to make life easier!
    pos=[]
    for i in range(len(text)):
        if text[i]==char: pos.append(str(i))
    return pos

def chaos(text,key): # returns back the original text from group()
    t=0; li=remshield(text).split('|')
    for i in li:
        c=len(i)
        if c>t: t=c
    ph=[False]*t; i=0
    for i in li:
        p=i[0]; pos=pick(i,'1')
        for j in pos:
            ph[int(j)]=p
    unknown=pick(ph,False)
    return ''.join(ph[1:])
