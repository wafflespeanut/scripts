from User import *

def compChooseWord(hand,wordList,n):
    maxi=0; best=""
    for word in wordList:
        if isValidWord(word,hand,wordList) and getWordScore(word, n)>maxi:
            best=word; maxi=getWordScore(word,n)
    return best

def compPlayHand(hand, wordList, n):
    total=0; word=""
    while (len(str(dispHand(hand)))>1):
        print "Current hand: " +dispHand(hand)
        word=compChooseWord(hand,wordList,n)
        if isValidWord(word,hand,wordList):
            total+=getWordScore(word,n)
            print '"'+word+'"' +" earned "+ str(getWordScore(word,n))+ " points. Total: " +str(total) +" points\n"
            hand=updateHand(hand,word)
        else: break
    print "Total score: " +str(total) +" points"
    
def playBoth(wordList):
    r=0; s=''
    while s!='e':
        s=raw_input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ")    
        if s=='r' and r==0:
            print "You have not played a hand yet. Please play a new hand first!\n"
        while s=='r' and r==1:
            pmt=raw_input("\nEnter u to have yourself to play, c to have the computer play: ")
            if pmt=='u':
                hand=handcopy.copy()
                playHand(hand, wordList, HAND_SIZE)
                break
            elif pmt=='c':
                hand=handcopy.copy()
                compPlayHand(hand, wordList, HAND_SIZE)
                break
            else: print "Invalid command.\n"
        while s=='n':
            pmt=raw_input("\nEnter u to have yourself to play, c to have the computer play: ")
            if pmt=='u':
                hand=dealHand(HAND_SIZE)
                handcopy=hand.copy()
                playHand(hand,wordList,HAND_SIZE)
                r=1; break
            elif pmt=='c':
                hand=dealHand(HAND_SIZE)
                handcopy=hand.copy()
                compPlayHand(hand, wordList, HAND_SIZE)
                r=1; break
            elif (pmt!='c' and pmt!='u'): print "Invalid command.\n"
        if (s!='e' and s!='n' and s!='r'): print "Invalid command.\n"
                
wordList=loadWords()
playBoth(wordList)
