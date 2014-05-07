import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {'a':1,'b':3,'c':3,'d':2,'e':1,'f':4,'g':2,'h':4,'i':1,'j':8,'k':5,'l':1,'m':3,'n':1,'o':1,'p':3,'q':10,'r':1,'s':1,'t':1,'u':1,'v':4,'w':4,'x':8,'y':4,'z':10}

WORDLIST_FILENAME = "Words.txt"

def loadWords():
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList
	
def getWordScore(word, n):
    count=0
    for ch in word:
        count+=SCRABBLE_LETTER_VALUES[ch]
    count*=len(word)
    if n==len(word):
        count+=50
    return count

def dealHand(n):
    hand={}
    numVowels = n / 3
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1   
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
    return hand

def updateHand(hand,word):
    handa=hand.copy()
    for cha in handa.keys():
        for ch in word:
            if cha==ch:
                handa[cha]-=1
    return handa

def isValidWord(word, hand, wordList):
    p=0
    handb=hand.copy()
    wordcp=""
    for a in word:
        wordcp+=a
    for ch in wordcp:
        for cha in handb.keys():
            if ch==cha and handb[cha]>0:
                p+=1
                handb[cha]-=1
                break
            else:
                continue
    return (p==len(wordcp) and (wordcp in wordList))

def dispHand(hand):
    char=""
    handd=hand.copy()
    for let in handd.keys():
        for j in range(handd[let]):
             char+=let+" "
    return char

def playHand(hand, wordList, n):
    total=0
    word=""
    while dispHand(hand):
        cp=0
        print "Current hand: " +dispHand(hand)
        word=raw_input('Enter word, or a "." to indicate that you are finished: ').lower()
        if word==".":
            print "Goodbye! Total score: " +str(total) +" points\n"
            cp=0
            break
        elif isValidWord(word,hand,wordList):
            cp=1
            total+=getWordScore(word,n)
            print '"'+word+'"' +" earned "+ str(getWordScore(word,n))+ " points. Total: " +str(total) +" points\n"
            hand=updateHand(hand,word)
        else:
            print "Invalid word, please try again.\n"
            cp=0
    if cp==1:
        print "Run out of letters. Total score: " +str(total) +" points"

def playGame(wordList):
    r=0
    s=' '
    while s!='e':
        s=raw_input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ")
        if s=='r' and r==0:
            print "You have not played a hand yet. Please play a new hand first!\n"
        elif s=='r' and r==1:
            hand=handcopy.copy()
            playHand(hand,wordList,HAND_SIZE)
        elif s=='n':
            hand=dealHand(HAND_SIZE)
            handcopy=hand.copy()
            playHand(hand,wordList,HAND_SIZE)
            r=1
        elif s!='e': print "Invalid command."
