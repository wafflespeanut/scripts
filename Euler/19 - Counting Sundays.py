months={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
sunday=6 # First Sunday is on 6th January 1901

def days(initial,lo,up):
    c=0; d=initial; k=0; a=[]
    for y in range(lo,up+1):
        if y%100==0:
            if y%400==0: months[2]=29
            else: months[2]=28
        elif y%4==0: months[2]=29
        else: months[2]=28
        for m in range(1,13):
            while d<months[m]:
                if d==1: c+=1
                d+=7; k+=1
            d-=months[m]
    a+=[c,k]
    return a

day=days(sunday,1901,2000)
print "Number of Sundays on the first month of 20th century: " +str(day[0])+ " out of " +str(day[1])+ " Sundays"
