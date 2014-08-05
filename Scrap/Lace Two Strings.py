def lace(s1, s2):
    m=""; i=0
    j=min(len(s1),len(s2))
    k=max(len(s1),len(s2))
    while i<j:
        m+=s1[i]+s2[i]
        i+=1
    if len(s1)>len(s2):
        m+=s1[i:k]
    else: m+=s2[i:k]
    return m

def laceRecur(s1, s2):
    def helps(s1, s2, out):
        if s1 == '':
            return out+s2
        if s2 == '':
            return out+s1
        else:
            return helps(s1[1:],s2[1:],out+s1[0]+s2[0])
    return helps(s1, s2, '')

