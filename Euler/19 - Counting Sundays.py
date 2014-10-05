months={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

def isLeap(y):
    if y%100==0:
        if y%400==0: return True
        else: return False
    elif y%4==0: return True
    return False

def sunday(year):        # To find the first Sunday of an year
    day=str(raw_input("Enter a known Sunday (in the form YYYY-MM-DD): "))
    y=int(day[:4]); m=int(day[5:7]); d=int(day[8:10])
    while all([y>=year,m>=1,d>=1]):
        if isLeap(y): months[2]=29
        else: months[2]=28
        while m>=1:
            if d>7: d-=7
            elif d<=7:
                if m>1: m-=1; d+=months[m]
                elif m==1: y-=1; m=12; d+=months[m]; break
    d-=months[1]
    print "\nFirst Sunday is on 0"+str(d)+'-01-'+str(year)+'!'
    return d

def count(l,u):          # Requires first Sunday for calculation!
    c=0; d=sunday(l); k=0; a=[]
    for y in range(l,u+1):
        if isLeap(y): months[2]=29
        else: months[2]=28
        for m in range(1,13):
            while d<months[m]:
                if d==1: c+=1
                d+=7; k+=1
            d-=months[m]
    a+=[c,k]
    return a

#s=count(1901,2000); print "Number of Sundays on the first month of 20th century: " +str(s[0])+ " out of " +str(s[1])+ " Sundays"
