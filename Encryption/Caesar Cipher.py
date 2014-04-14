import string
import random

WORDLIST_FILENAME = "Words.txt"

def loadWords():
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = inFile.read().split()
    print "  ", len(wordList), "words loaded."
    return wordList

def isWord(wordList, word):
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in wordList

def buildCoder(shift):
    s=shift
    if int(shift)>26:
        s%=26
    letters={}
    temp={}
    group1=string.ascii_uppercase
    group2=string.ascii_lowercase
    for i in range(26):
        if i+s < 26:
            letters[group1[i]]=group1[i+s]
            temp[group2[i]]=group2[i+s]
        else:
            letters[group1[i]]=group1[i+s-26]
            temp[group2[i]]=group2[i+s-26]
    letters.update(temp)
    return letters

def applyCoder(text, coder):
    code=coder.copy()
    char=""
    for cha in text:
        for ch in code.keys():
            if ch==cha:
                char+=code[cha]
            elif cha in string.punctuation or cha in string.digits or cha==" ":
                char+=cha
                break
    return char

def applyShift(text, shift):
    return applyCoder(text,buildCoder(shift))
    
def findBestShift(wordList, text):
    t=text
    real=0
    best=0
    m=0
    for i in range(25):
        t=applyShift(t,1)
        split=t.split(' ')
        for j in range(len(split)):
            if isWord(wordList,split[j]):
                m+=1
        if m>real:
            m=real
            best=i+1
    return best

wordList = loadWords()
s=applyShift('Hello, world!',8)
print "Shift-8 applied for 'Hello world': " +s
bestShift=findBestShift(wordList,s)
print "Best shift found: " +str(bestShift)
print "Reapplying shift(" +str(bestShift) +")"
if applyShift(s, bestShift)=='Hello, world!':
    print "True"
else: print "False"
