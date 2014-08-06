def transpose(phr):
    punc=string.punctuation; c=False
    for i in phr:
        if i in punc:
            l=int(len(phr)**0.5); c=True
        else: l=int(len(phr)**0.5)+1
    m=0; n=len(phr)
    trans=[[0 for x in range(l)] for j in range(l)]
    mat=[phr[i:(i+l)] for i in range(m,n,m+l)]
    for i in range(len(mat)):
        while len(mat[i])<l: mat[i]+=random.choice(punc)
    for i in range(l):
        for j in range(l):
            trans[i][j]=mat[j][i]
    for i in range(l):
        trans[i]=''.join(trans[i])
    tp=''.join(trans)
    if c==True:
        while tp[-1] in punc: tp=tp[:-1]
    return tp
