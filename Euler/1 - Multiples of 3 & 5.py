a=[]; s=0
for i in range(334):
    if 3*i<1000: a+=[3*i]
    if 5*i<1000: a+=[5*i]

for i in list(set(a)):
    s+=i

# print '''The sum of multiples of 3 "or" 5 below 1000: ''' +str(s)
