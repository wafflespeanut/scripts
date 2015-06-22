execfile("12 - Highly Divisible Triangular Number.py")
execfile("22 - Names Scores.py")

def triscores(words):
    s=0; triangles=[tri(i) for i in range(1,25)]
    for i in words:
        score=0
        for j in i: score+=ord(j)-64
        if score in triangles: s+=1
    return s

#words=load("WORDS.txt"); s=triscores(words); print "There are " +str(s)+ " triangle words in the text file!"
