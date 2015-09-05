import os, random, string

WORDLIST = os.path.realpath("../Crypto/Words.txt")

def loadWords():
    print "Loading words from the list..."
    inFile = open(WORDLIST, 'r', 0)
    line = inFile.readline()
    wordlist = string.split(line)
    print len(wordlist), "words loaded."
    return wordlist

def chooseWord(wordlist):
    return random.choice(wordlist)

wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
    if all((ch in lettersGuessed) for ch in secretWord):
        return True
    else:
        return False

def isletterGuessed(secretWord, lettersGuessed):
    if any((ch in lettersGuessed) for ch in secretWord):
        return True
    else:
        return False

def alreadyGuessed(lettersGuessed, letter):
    if lettersGuessed.count(letter) > 1:
        return True
    else:
        return False

def getGuessedWord(secretWord, lettersGuessed):
    word = ''
    for ch in secretWord:
        i = (''.join(lettersGuessed)).find(ch)
        if i != -1:
            word += ch
        elif i == -1:
            word += "_"
    return word

def getAvailableLetters(lettersGuessed):
    default = "abcdefghijklmnopqrstuvwxyz"
    for ch in lettersGuessed:
        default = default.replace(ch, "")
    return default

def hangman(secretWord):
    mistakesMade = 0
    lettersGuessed = ''
    print "\nWelcome to the game Hangman!"
    print "I'm thinking of a word that is", str(len(secretWord)), "letters long."
    while mistakesMade < 8 or isWordGuessed(secretWord, lettersGuessed):
        print " --  --  --  --  --  -- "
        print "You have", str(8 - mistakesMade), "guesses left."
        print "Available letters:", getAvailableLetters(lettersGuessed)
        letter = raw_input("Please guess a letter: ").lower()
        lettersGuessed += letter
        if alreadyGuessed(lettersGuessed, letter):
            print "Oops! You've already guessed that letter:", getGuessedWord(secretWord, lettersGuessed)
        elif isletterGuessed(secretWord, letter):
            print "Good guess!", getGuessedWord(secretWord, lettersGuessed)
            if isWordGuessed(secretWord, lettersGuessed):
                print " --  --  --  --  --  -- \nCongratulations, you've won!"
                break
        else:
            print "Oops! That letter is not in my word!", getGuessedWord(secretWord, lettersGuessed)
            mistakesMade += 1
    if mistakesMade == 8:
        print " --  --  --  --  --  -- \nSorry, you ran out of guesses. The word was " + secretWord

secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
