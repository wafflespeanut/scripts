def getGrid():
    a=[]; t=raw_input("Enter the raw grid input...\n")
    a.append(str(t))
    return ''.join(a).split('\n')

def checkSide(grid):
    i=0; s=0; t=0
    while i<len(grid):
        get=[]
        for j in grid[i].split(' '):
            get.append(int(j))
        for a in range(len(get)-3):
            s=get[a]*get[a+1]*get[a+2]*get[a+3]
            if s>t: t=s
        i+=1
    return t

def gridTrans(grid):
    i=0; push=[]; get=[]
    while i<len(grid[0].split(' ')):
        get.append(grid[i].split(' ')); i+=1
    for i in range(len(get)):
        s=[]
        for j in range(len(get[i])):
            s.append(get[j][i])
        push.append(' '.join(s))
    return checkSide(push)

def leftDiagonal(grid,k):
    i=0; s=0; t=0; get=[]
    while i<len(grid[0].split(' ')):
        get.append(grid[i].split(' ')); i+=1
    i=k-1; fin=[]
    while i<len(get):
        m=i; n=0; s=[]
        while n<=i:
            s.append(get[m][n])
            m-=1; n+=1
        fin.append(' '.join(s)); i+=1
    for i in range(len(get)-k):
        m=len(get)-1; n=i+1; s=[]
        while m>=i+1:
            s.append(get[m][n])
            m-=1; n+=1
        fin.append(' '.join(s))
    return checkSide(fin)

#grid=getGrid(); final=max(checkSide(grid),gridTrans(grid),leftDiagonal(grid,4))
#print "The greatest product of four adjacent numbers in the same direction (vertical, horizontal & diagonal) is " +str(final)
