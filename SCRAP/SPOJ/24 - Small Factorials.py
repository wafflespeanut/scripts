def fact(n):
    i=2; k=1
    while i<=n: k*=i; i+=1
    return k

t=int(raw_input()); k=0
while k<t:
    s=int(raw_input())
    print fact(s)
    k+=1

