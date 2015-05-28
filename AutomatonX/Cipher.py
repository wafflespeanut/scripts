import random, timeit, os

def sieve(n):                                       # Generates a list of primes using the sieve of Eratosthenes
    primes = [False] * 2 + [True] * (n - 1)
    for i in range(int(n ** 0.5) + 1):
        if primes[i]:
            for j in range(i * i, n + 1, i):
                primes[j] = False
    return [prime for prime, index in enumerate(primes) if index]

def CXOR(text, key):                                # Quite useful for XOR'ing bulk text & key
    def xor(char1, char2):              # XORs two characters
        return chr(ord(char1) ^ ord(char2))
    i = 0
    j = 0
    result = ""
    while i < len(text):              # if len(key) < len(text)
        if i < len(key):
            result += xor(text[i], key[j])
        else:
            j = 0
            result += xor(text[i], key[j])
        i += 1
        j += 1
    i = 0
    j = 0
    while i < len(key):                 # if len(text) < len(key)
        if i < len(text):
            result = result[:j] + xor(text[j], key[i]) + result[j+1:]
        else:
            j = 0
            result = result[:j] + xor(text[j], key[i]) + result[j+1:]
        i += 1
        j += 1
    return result

def hexed(text):                                    # Hexing function
    return map(lambda i:
        format(ord(i), '02x'), list(text))

def add(text, key):                                 # Adds the ASCII values of key and text chars
    listedText = list(''.join(text))
    listedKey = list(key)
    num = list("0123456789")
    i = len(key) - 1
    for a, b in enumerate(listedText):
        if b in num:
            if i == 0:
                i = len(key) - 1
            listedText[a] = str(int(b) + ord(listedKey[i]))[-1]
            i -= 1
    return ''.join(listedText)

def throwPrimeBlock(text, level):                   # Generates a giant block of primes based on the ASCII values of key chars
    def primeList(level):                   # Calls the sieve for generating prime lists based on strength
        k = 2 ** (5 + level)
        return sieve(k * k)
    primes = []
    plist = primeList(level / 2)
    for k in text:
        primes += [str(plist[ord(k)])]
    for n in range(level):                  # Join the blocks
        block = []
        block += ''.join(primes)
        for i, j in enumerate(block):
            primes += [str(plist[int(j)])]
    return ''.join(primes)

def popNum(text, level):                            # Confuses & constrains the sliced list to 8-chars
    merged = []
    block = throwPrimeBlock(text, level)
    while len(block) >= 8:                  # Only because I love "8" next to "2"
        merged.append(block[0:8])
        block = block[8:]
    return list(set(merged))

def combine(text, key):                             # Dissolves key chars into the text
    try:
        added = add(hexed(text), key)
    except IndexError:
        return None
    return ''.join(added)

def char(text):                                     # Hex-decoding function
    split = [text[i:i+2] for i in range(0, len(text), 2)]
    try:
        return ''.join(i.decode('hex') for i in split)
    except TypeError:
        return None

def sub(text, key):                                 # Subtracts the key and gets text chars back!
    try:
        listedText = list(''.join(text))
        listedKey = list(key)
        num = list("0123456789")
        i = len(key) - 1
        for x, ch in enumerate(listedText):         # Executes from the last char
            if ch in num:
                if i == 0:
                    i = len(key) - 1
                listedText[x] = str((10 + int(ch)) - int(str(ord(listedKey[i]))[-1]))[-1]
                i -= 1
        out = ''.join(listedText)
    except TypeError:
        return None
    return out

def find(text, key, level):                         # Finds the random key used during encryption (using caught exceptions)
    nums = popNum(key, level)
    for i, value in enumerate(nums):
        rkey = combine(value, key)
        if extract(extract(text, rkey), key) is not None:
            return extract(text, rkey)
        else:
            continue
    return None

def extract(text, key):                             # Removes the key chars from the text
    try:
        return ''.join(char(sub(text, key)))
    except TypeError:
        return None

def shift(text, shift):                             # Shifts the ASCII value of the chars (Vigenere cipher? Yep!)
    try:
        shiftedText = ''
        for i, ch in enumerate(text):
            shiftChar = ord(ch) + shift
            while shiftChar > 255:
                shiftChar -= 255
            shiftedText += chr(shiftChar)
    except TypeError:
        return None
    return shiftedText

def encrypt(text, key, iteration):                  # Iteration, shifting, random key, etc.
    i = 1
    cipherText = combine(text, key)
    uniqueNums = popNum(key, iteration)
    random.shuffle(uniqueNums)
    chosenKey = combine(random.choice(uniqueNums), key)
    if i < iteration:
        while i < iteration:
            cipherText = combine(cipherText, key)
            i += 1
    cipherText = combine(cipherText, chosenKey)
    if cipherText == None:
        return None
    shiftedText = cipherText
    hexedKey = ''.join(hexed(key))
    for i in key:
        shiftedText = shift(shiftedText, ord(i))
    finalRound = add(shiftedText, key)
    xor = CXOR(finalRound, hexedKey)
    return ''.join(hexed(xor))

def decrypt(text, key, iteration):                  # The whole eit() thing in reverse...
    hexedKey = ''.join(hexed(key))
    xor = CXOR(char(text), hexedKey)
    shiftedText = sub(xor, key)
    for k in key:
        shiftedText = shift(shiftedText, 255 - ord(k))
    i = 1
    textBlocks = find(shiftedText, key, iteration)
    while i < iteration:
        textBlocks = extract(textBlocks, key)
        i += 1
    plainText = extract(textBlocks, key)
    if plainText == None:
        return None
    return plainText

def process(mode, text, key, level):
    if mode == 'e':
        finalText = encrypt(text, key, int(level))
    elif mode == 'd':
        finalText = decrypt(text, key, int(level))
    if finalText == None:
        return None
    else:
        return str(finalText)

def ask():
    key = raw_input("Password: ")
    while len(key) == 1 or key == "":
        if not key:
            print "\n No password? You do want me to encrypt, right?\n"
            key = str(raw_input("What's the password? "))
        elif len(key) == 1:
            print "\n No, Seriously? Password of unit length? Try something bigger...\n"
            key = str(raw_input("Choose a password: "))
    level = raw_input("Security level (1-5, for fast output): ")
    while level == '' or level not in '12345':
        print "\n Enter a number ranging from 1-5!\n"
        level = raw_input("Security level (1-5): ")
    mode = raw_input("Encrypt (e) or Decrypt (d)? ")
    while mode is not "e" and mode is not "d":
        print "\n (sigh) You can choose something...\n"
        mode = raw_input("Encrypt (e) or Decrypt (d)? ")
    return key, level, mode

def RUN():                                          # User Interface
    try:
        choice = 'y'
        while choice == 'y':
            text = raw_input("\nText to put in the cipher: ")
            while text == "":
                print "\n Um, I don't see any text here... Gimme something to eat!!!"
                text = raw_input("\nText to be encrypted: ")
            key, level, mode = ask()
            if mode == 'e':
                print "\nENCRYPTING...\n"
            elif mode == 'd':
                print "\nDECRYPTING...\n"
            start = timeit.default_timer()
            output = process(mode, text, key, level)
            stop = timeit.default_timer()
            if output == None:
                print "\tMismatch between ciphertext and key!!!\n\nPossibly due to:\n\t- Incorrect key (Check your password!)\n\t- Varied iterations (Check your security level!)\n\t(or) such an exotic ciphertext doesn't even exist!!! (Testing me?)\n"
            else:
                print "TOTAL TIME:", round(stop - start, 5), "seconds"
                print '\nMESSAGE: %s\n' % (output)
            choice = raw_input("Do something again: (y/n)? ")
    except KeyboardInterrupt:
        return None

def FILE():                                         # Encrypts/Decrypts text files
    try:
        while True:
            path = raw_input("Enter File name (including path): ")
            try:
                File = open(path, 'r')
                File.close()
                break
            except IOError:
                print "\n INVALID PATH!\n"
        key, level, mode = ask()
        if mode == 'e':
            print "\nENCRYPTING...\n"
        elif mode == 'd':
            print "\nDECRYPTING...\n"
        start = timeit.default_timer()
        newline = None
        with open(path, 'r') as file:               # Encrypts/decrpts line by line
            data = file.readlines()
        if len(data) == 0:
            print "Nothing in file!"
            return None
        for i in range(len(data)):                  # Correction for linux-based OS
            if data[i] == '\n' or data[i] == '\r\n':
                i += 1
                continue
            if data[i][-2:] == '\r\n':
                data[i] = process(mode, str(data[i][:-2]), key, level)
                newline = True
            elif data[i][-1] == '\n':
                data[i] = process(mode, str(data[i][:-1]), key, level)
                newline = True
            else:
                data[i] = process(mode, str(data[i]), key, level)
                newline = False
            if data[i] == None:
                print "\tMismatch between ciphertext and key!!!\n\nPossibly due to:\n\t- Incorrect key (Check your password!)\n\t- Varied iterations (Check your security level!)\n\t(or) such an exotic ciphertext doesn't even exist!\n"
                return None
            if newline and '/bin' in os.path.defpath:
                data[i] += '\r\n'
            elif newline:
                data[i] += '\n'
        with open(path, 'w') as file:
            file.writelines(data)
        stop = timeit.default_timer()
        print "TOTAL TIME:", round(stop - start, 5), "seconds"
    except KeyboardInterrupt:
        return None
