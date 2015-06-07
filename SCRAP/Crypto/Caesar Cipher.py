import string
from random import choice

def loadWords():
    print "Loading word list from file..."
    inFile = open("Words.txt", 'r')
    wordList = inFile.read().split()
    print "  ", len(wordList), "words loaded.\n"
    return wordList

def isWord(wordList, word):
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in wordList

def buildCoder(shift):
    s = shift
    letters = {}
    temp = {}
    if int(shift) > 26:
        s %= 26
    group1 = string.ascii_uppercase
    group2 = string.ascii_lowercase
    for i in range(26):
        if i + s < 26:
            letters[group1[i]] = group1[i + s]
            temp[group2[i]] = group2[i + s]
        else:
            letters[group1[i]] = group1[i + s - 26]
            temp[group2[i]] = group2[i + s - 26]
    letters.update(temp)
    return letters

def applyCoder(text, coder):
    code = coder.copy()
    char = ""
    for cha in text:
        for ch in code.keys():
            if ch == cha:
                char += code[cha]
            elif cha in string.punctuation or cha in string.digits or cha == " ":
                char += cha
                break
    return char

def applyShift(text, shift):
    return applyCoder(text, buildCoder(shift))

def findBestShift(wordList, text):
    t = text
    real = 0
    best = 0
    m = 0
    for i in range(25):
        t = applyShift(t, 1)
        split = t.split(' ')
        for j in range(len(split)):
            if isWord(wordList, split[j]):
                m += 1
        if m > real:
            m = real
            best = i + 1
    return best

if __name__ == '__main__':
    wordList = loadWords()
    n = choice(range(26))
    s = applyShift('Hello, world!', n)
    print "Shift-%d applied for 'Hello world': " % (n) + s
    bestShift = findBestShift(wordList, s)
    print "\nBest shift found: " + str(bestShift)
    print "Reapplying shift(" + str(bestShift) + ")...\n"
    if applyShift(s, bestShift) == 'Hello, world!':
        print True
    else:
        print False
