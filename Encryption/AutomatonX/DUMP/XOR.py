def xor(ch1,ch2): # XOR's characters (deprecated since when I found inbuilt XOR)
    a=bin(ord(ch1))[2:]; b=bin(ord(ch2))[2:]; p=0; kill=""
    if len(a)>len(b): b=(len(a)-len(b))*'0'+b
    elif len(a)<len(b): a=(len(b)-len(a))*'0'+a
    while p<len(a):
        q=int(a[p])+int(b[p])
        if q==2: kill+='0'
        else: kill+=str(q)
        p+=1
    return chr(int(kill,2))
