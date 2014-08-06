import random
import string

WORDLIST_FILENAME="Words.txt"

def loadWords():
    print "Loading words from the list..."
    inFile=open(WORDLIST_FILENAME,'r',0)
    line=inFile.readline()
    wordlist=string.split(line)
    print len(wordlist),"words loaded."
    return wordlist

def chooseWord(wordlist):
    return random.choice(wordlist)

wordlist=loadWords()

def isWordGuessed(secretWord,lettersGuessed):
    if all((c in lettersGuessed) for c in secretWord): return True
    else: return False

def isletterGuessed(secretWord,lettersGuessed):
    if any((c in lettersGuessed) for c in secretWord): return True
    else: return False

def alreadyGuessed(lettersGuessed,letter):
    if lettersGuessed.count(letter)>1: return True
    else: return False

def getGuessedWord(secretWord,lettersGuessed):
    s=''
    for c in secretWord:
        l=(''.join(lettersGuessed)).find(c)
        if l!=-1: s+=c
        elif l==-1: s+="_"
    return s

def getAvailableLetters(lettersGuessed):
    default="abcdefghijklmnopqrstuvwxyz"
    for ch in lettersGuessed:
        default=default.replace(ch,"")
    return default    

def hangman(secretWord):
    mistakesMade=0
    lettersGuessed=''
    print "\nWelcome to the game Hangman!"
    print "I'm thinking of a word that is " +str(len(secretWord)) +" letters long."
    while mistakesMade<8 or isWordGuessed(secretWord,lettersGuessed):
        print "------------"
        print "You have " +str(8-mistakesMade) +" guesses left."
        print "Available letters: " +getAvailableLetters(lettersGuessed)
        letter=raw_input("Please guess a letter:").lower()
        lettersGuessed+=letter
        if alreadyGuessed(lettersGuessed,letter):
            print "Oops! You've already guessed that letter: " +getGuessedWord(secretWord,lettersGuessed)
        elif isletterGuessed(secretWord,letter):
            print "Good guess:" +getGuessedWord(secretWord,lettersGuessed)
            if isWordGuessed(secretWord,lettersGuessed):
                print "------------\nCongratulations, you won!"
                break
        else:
            print "Oops! That letter is not in my word: " +getGuessedWord(secretWord,lettersGuessed)
            mistakesMade+=1
    if mistakesMade==8:
        print "------------\nSorry, you ran out of guesses. The word was " +secretWord

secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
