def laceStrings(s1, s2):
    m=""
    i=0
    j=min(len(s1),len(s2))
    k=max(len(s1),len(s2))
    while i<j:
        m+=s1[i]+s2[i]
        i+=1
    if len(s1)>len(s2):
        m+=s1[i:k]
    else: m+=s2[i:k]
    return m

print laceStrings("wxyzk","efghi")
