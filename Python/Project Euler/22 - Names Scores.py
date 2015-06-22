def load(stuff):
    print "Loading names from file..."
    File=open(stuff,'r',0); List=""
    for i in File: List+=i
    List=(''.join(List.split('"'))).split(',')
    print "  ",len(List),"words loaded.\n"
    return sorted(List)

def scores(names):
    score=0; i=0
    while i<len(names):
        wsc=0
        for j in names[i]: wsc+=ord(j)-64
        score+=wsc*(i+1); i+=1
    return score

#names=load("NAMES.txt"); print "The total of all name scores in the text file is: " +str(scores(names))
