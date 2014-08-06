a=[]; i=100; j=100; final=[]

while i<=999:
    while j<=999:
        a.append(str(i*j)); j+=1
    i+=1; j=100

for i in a:
    s=""
    for j in i:
        s=j+s
    if s==i: final.append(int(i))

print "The largest palindrome of product of two 3-digit numbers:" +max(final)
