def collatz(n):
    i=n; a=[]
    while i!=1:
        if i%2==0: i=i/2
        else: i=3*i+1
        a.append(i)
    return a

def longest(n):
    i=2; t=[0,0]
    while i<=n:
        c=collatz(i)
        if len(c)>t[1]: t[1]=len(c); t[0]=i
        i+=1
    return t

print longest(1000000)
