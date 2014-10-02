def find():
    c=0
    for i in range(1,10):   # Find out why it can't exceed 9!
        j=1
        while len(str(i**j))==j: c+=1; j+=1
    return c

#s=find(); print 'There are',s,'n-digit numbers which are also an nth power!'
