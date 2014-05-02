s="nkdvbcdepjweolypqrstuvkzzy"
out=''
temp=''
for char in s:
    if temp=='':
        temp=char
    if temp[-1]<=char:
        temp+=char
    elif temp[-1]>char:
        if len(out)<len(temp):
            out=temp
            temp=char
        else:
            temp=char
if len(temp)>len(out):
           out=temp
    
print "Longest substring in alphabetical order is: " +out
