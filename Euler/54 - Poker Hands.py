# Firstly, we need something to sort things up!
score={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}

def hands(stuff):
    print "Loading from file..."
    File=open(stuff,'r',0); List=[]
    for i in File: List.append([i[:14],i[15:-1]])
    print "  ",len(List),"hands loaded.\n"
    return List

def high(s):
    a=''; r=0
    for i,j in enumerate(s):
        if j in score and score[j]>r: r=score[j]; a=s[i]
    return a

def pair(s):
    a=[i for i in s if i in score]; k=[]
    for i in set(a):
        if a.count(i)>1: k.append([i,a.count(i)])
    if len(k)==1: return k[0]
    elif len(k)>1: return k
    else: return None

def suit(s):
    a=set([s[i] for i in range(1,len(s),3)])
    if len(a)>1: return False
    else: return True

def royal(s):
    a=['T','J','Q','K','A']
    for i in a:
        if i not in s: return False
    return True

def consec(s):
    a=sorted([score[i] for i in s if i in score]); i=0
    while i<len(a)-1:
        if not a[i+1]==a[i]+1: return False
        i+=1
    return True

def checkhigh(s):
    a=high(s[0]); b=high(s[1])
    if score[a]>score[b]: return 1
    else: return 2

def checksf(s):
    if all([consec(s[0]) and suit(s[0]),consec(s[1]) and suit(s[1])]): return checkhigh(s)
    elif all([consec(s[0]),suit(s[0])]): return 1
    elif all([consec(s[1]),suit(s[1])]): return 2
    else: return None

def three(s):
    k=pair(s)
    if k:
        if len(k[0])>1:
            if 3 in k[0] or 3 in k[1]: return True
        elif len(k[0])==1:
            if 3 in k: return True
    return False

def twop(s):
    k=pair(s)
    if k:
        if len(k)>1 and len(k[0])>1:
            if 2 in k[0] and 2 in k[1] and k[0][0]!=k[1][1]: return True
    return False

def two(s):
    k=pair(s)
    if k:
        if len(k[0])>1:
            if 2 in k[0] or 2 in k[1]: return True
        elif len(k[0])==1:
            if 2 in k: return True
    return False

def four(s):
    if all([pair(s[0]),pair(s[1])]):
        if 4 in pair(s[0]) and 4 in pair(s[1]): return checkhigh(s)
        elif 4 in pair(s[0]): return 1
        elif 4 in pair(s[1]): return 2
    return None

def house(s):
    if all([two(s),three(s)]): return True
    return False

def life(f,s):      # Reused a heck of times!
    if f(s[0]) and f(s[1]): return clife(f,s)
    elif f(s[0]): return 1
    elif f(s[1]): return 2
    return None

def clife(f,s):     # Life's tough! Should check high cards inside pairs...
    if f(s[0]) and f(s[1]):
        k1=pair(s[0]); k2=pair(s[1])
        if f==house or f==three:
            c1=''; c2=''
            for i in k1:
                if 3 in i: c1=i[0]
            for i in k2:
                if 3 in i: c2=i[0]
            if score[c1[0]]>score[c2[0]]: return 1
            elif score[c1[0]]<score[c2[0]]: return 2
        elif f==two:
            if score[k1[0]]>score[k2[0]]: return 1
            elif score[k1[0]]<score[k2[0]]: return 2
            elif score[k1[0]]==score[k2[0]]:
                a=s[0].replace(k1[0],' '); b=s[1].replace(k2[0],' ')
                return checkhigh([a,b])
        return checkhigh(s)

def find(s):
    if royal(s[0]): return 1
    elif royal(s[1]): return 2
    if checksf(s): return checksf(s)
    if four(s): return four(s)
    if life(house,s): return life(house,s)
    if life(suit,s): return life(suit,s)
    if life(consec,s): return life(consec,s)
    if life(three,s): return life(three,s)
    if life(twop,s): return life(twop,s)
    if life(two,s): return life(two,s)
    return checkhigh(s)

def poker():
    play=hands('POKER.txt'); p1=0
    for s in play:
        if find(s)==1: p1+=1
    return p1

#print "Player 1 has won " +str(poker())+ " times!"
