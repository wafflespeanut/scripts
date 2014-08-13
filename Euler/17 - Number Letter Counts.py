def letters(n):
    coll={0:10,1:3,2:3,3:5,4:4,5:4,6:3,7:5,8:5,9:4,10:3,11:6,12:6,13:8,14:8,15:7,16:7,17:9,18:8,19:8,20:6,30:6,40:5,50:5,60:5,70:7,80:6,90:6,100:7,1000:8}
    return coll[n]

def wordlen(n):
    a=str(n); s=0; i=n
    if len(a)==1: s+=letters(n)
    def two(k):
        b=str(k); f=0
        if k%10==0 or k<20: f+=letters(k)
        else: f+=letters(int(b[0]+'0'))+letters(k%10)
        return f
    if len(a)==2: s=two(i)
    elif len(a)==3:
        if i%100==0: s+=letters(i/100)+letters(100)
        elif len(str(i%100))==2: s+=letters(i/100)+two(i%100)+letters(0)
        else: s+=letters(i/100)+letters(0)+letters(i%100)
    elif i%1000==0: s+=letters(i/1000)+letters(1000)
    return s

def run(n):
    s=0
    for i in range(1,n+1):
        s+=wordlen(i)
    return s
