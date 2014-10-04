def solve(n):
    i=2
    if int(n**0.5)==n**0.5: return None
    while True:
        k=(1+n*i**2)**0.5
        if k==int(k): return [int(k),i]
        i+=1
    return None

def find(r):
    t=[0,0]
    try:
        for i in range(2,r+1):
            k=solve(i)
            if k and k[0]>t[1]: t[1]=k[0]; t[0]=i
        return t
    except KeyboardInterrupt: return i
