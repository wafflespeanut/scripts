execfile("49 - Prime Permutations.py")

def shift(s1,s2):     # Historical significance
    a=[s1+s2]; k=len(s1); c=0
    def left(s,d): a=list(s); a[d-1],a[d]=a[d],a[d-1]; return ''.join(a)
    while len(a)<len(s1)*len(s2):
        i=len(s1)+c
        while i>0: a.append(left(a[-1],i)); i-=1
        if i==0 and i<len(a[0]): c+=1
    return a

def family():       # I'm being steeeupid!
    p=[i for i in ESieve(10**5-1,10**6-1) if str(i)[-1]=='3']
    r=3; a=[]; q=range(10**(r-2),10**(r-1)-1); n='0123456789'
    for i in q:
        m=0; t=[]
        for j in n:
            m=str(i)+r*j
            if int(m+'3') in p: t.append(int(m+'3'))
        if len(t)>len(a): a=t
        m=0; t=[]
        for j in n:
            m=j+str(i)+(r-1)*j
            if int(m+'3') in p: t.append(int(m+'3'))
        if len(t)>len(a): a=t
        m=0; t=[]
        for j in n:
            m=(r-1)*j+str(i)+(r-2)*j
            if int(m+'3') in p: t.append(int(m+'3'))
        if len(t)>len(a): a=t
        m=0; t=[]
        for j in n:
            m=j+str(i)[0]+j+str(i)[-1]+j
            if int(m+'3') in p: t.append(int(m+'3'))
        if len(t)>len(a): a=t 
    return a
