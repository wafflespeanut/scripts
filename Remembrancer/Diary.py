import os, subprocess
from time import sleep
from time import strftime as time
from random import choice

# Modified for my Ubuntu/Windows-8 dual-boot...

if '/bin' in os.path.defpath:
    ploc = '/media/' + os.path.expanduser('~').split('/')[-1] + '/Local Disk/Users/Waffles Crazy Peanut/AppData/Local/SYSTEM.DAT'
    loc = '/media/' + os.path.expanduser('~').split('/')[-1] + '/Local Disk/Users/Waffles Crazy Peanut/Desktop/Dropbox/Diary/'
else:
    ploc = os.path.expanduser('~') + '\\AppData\\Local\\SYSTEM.DAT'         # Password location
    loc = os.path.expanduser('~') + '\\Desktop\\Dropbox\\Diary\\'           # Storage location

months = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

def hexed(text):                                                # Hexing function
    return map(lambda i:
        format(ord(i), '02x'), list(text))

def hashed(stuff, bits = 32, rounds = 128):                     # Hashing a hexed string with specified rounds
    pad = bits - len(stuff) % bits                              # Padding is solely for fun!
    if not pad / 10:
        pad = '0' + pad
    t = ''.join(hexed(stuff)) + str(pad) * pad
    for i in range(rounds):
        t = hash(str(t))
    return str(abs(t))

def char(text):                                                 # Hex-decoding function
    split = [text[i:i+2] for i in range(0, len(text), 2)]
    try:
        return ''.join(i.decode('hex') for i in split)
    except TypeError:
        return None

def shift(text, shift):                                         # Shifts the ASCII value of the chars (Vigenere cipher? Yep!)
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

def zombify(mode, data, key):                                     # Linking helper function
    hexedKey = ''.join(hexed(key))
    text = data
    if mode == 'e':
        text = ''.join(hexed(data))
        for ch in hexedKey:
            text = shift(text, ord(ch))
        return text
    elif mode == 'd':
        for ch in hexedKey:
            text = shift(text, 255 - ord(ch))
        return char(text)

def temp(File, key = None):                                     # Uses default notepad to view stuff
    if File == None:
        return None
    if protect(File, 'd', key):
        subprocess.Popen(["notepad", loc + 'TEMP.tmp'])
        sleep(2)
        os.remove(loc + 'TEMP.tmp')

def check():                                                    # Allows password to be stored locally
    if not os.path.exists(ploc):
        try:
            k1 = True
            k2 = False
            while True:
                k1 = raw_input('\nEnter password: ')
                while len(k1) < 8:
                    k1 = raw_input('\nEnter password of at least 8 chars: ')
                k2 = raw_input('Re-enter password: ')
                if k1 == k2:
                    break
                else:
                    print "\nPasswords don't match!\n"
            key = k1 = k2
            for i in range(10):                                 # Nothing too serious, it just hexes the thing 10 times!
                key = ''.join(hexed(key))
            with open(ploc, 'w') as file:
                file.writelines(key)
        except KeyboardInterrupt:
            print 'Login credentials failed!'
            return None
    else:
        with open(ploc, 'r') as file:
            key = file.readlines()
        if key:
            key = key[0]
        else:
            return None
        for i in range(10):
            key = char(key)
    return key

def protect(path, mode, key = None):                              # A simple method which shifts and turns it to hex!
    if os.path.exists(ploc):
        key = check()
    try:
        if not key:
            key = raw_input('\nEnter password for your story: ')
        while len(key) < 8:
            key = raw_input('\nEnter password of at least 8 chars: ')
    except KeyboardInterrupt:
        return False
    with open(path, 'r') as file:
        data = file.readlines()
    if len(data) == 0:
        print 'Nothing in file!'
        return None
    try:
        for i in range(len(data)):
            if data[i] == '\n' or data[i] == '\r\n':            # The '\r\n' thing is for newline in linux-based OS
                i += 1
                continue
            if data[i][-2:] == '\r\n':
                data[i] = zombify(mode, str(data[i][:-2]), key)
                newline = True
            elif data[i][-1] == '\n':
                data[i] = zombify(mode, str(data[i][:-1]), key)
                newline = True
            else:
                data[i] = zombify(mode, str(data[i]), key)
                newline = False
            if newline and 'bin' in ploc:
                data[i] += '\r\n'
            elif newline:
                data[i] += '\n'
    except TypeError:
        print '\n\tWrong password!'
        return None
    if mode == 'e':
        with open(path, 'w') as file:
            file.writelines(data)
    elif mode == 'd':
        with open(loc + 'TEMP.tmp', 'w') as file:
            file.writelines(data)
    return key

def write(File = None):                                         # Does all the dirty job
    key = None
    if not File:
        File = loc + hashed('Day ' + time('%d') + ' (' + months[time('%m')] + ' ' + time('%Y') + ')')
    if os.path.exists(File) and os.path.getsize(File) != 0:
        print '\nFile already exists! Appending to current file...'
        while not key:
            key = protect(File, 'd')
            if not key:
                print 'A password is required to append to an existing file. Running sequence again...'
        with open(loc + 'TEMP.tmp', 'r') as file:
            data = file.readlines()
        with open(File, 'w') as file:
            file.writelines(data)
        os.remove(loc + 'TEMP.tmp')
    elif os.path.exists(File):
        os.remove(File)
    f = open(File, 'a')
    data = ['[' + time('%Y') + '-' + time('%m') + '-' + time('%d') + ']' + ' ' + time('%H') + ':' + time('%M') + ':' + time('%S') + '\n']
    try:
        stuff = raw_input('''\nStart writing... (Press Ctrl+C when you're done!)\n\n\t''')
        data.append('\t' + stuff)
    except KeyboardInterrupt:
        print 'Nothing written! Quitting...'
        protect(File, 'e', key)
        return None
    while True:
        try:
            stuff = raw_input()
            data.append(stuff)
        except KeyboardInterrupt:
            break
    f.write('\n'.join(data) + '\n\n')
    f.close()
    k = None
    if key:
        k = key
        key = None
    while not key:
        if k:
            key = k
        key = protect(File, 'e', key)
        if not key:
            print "\nPlease don't interrupt! Your story is insecure! Running sequence again..."
    choice = raw_input('\nSuccessfully written to file! Do you wanna see it (y/n)? ')
    if choice == 'y':
        temp(File, key)

def day():                                                      # Return a path based on (day,month,year) input
    while True:
        y = raw_input('\nYear: ')
        if len(y) == 4:
            break
    while True:
        s = raw_input('\nMonth: ')
        if s in months:
            m = months[s]
            break
        elif '0' + s in months:
            m = months['0' + s]
            break
    while True:
        s = raw_input('\nDay: ')
        if len(s) == 1:
            s = '0' + s
        if int(s) < 32:
            break
    fileName = loc + hashed('Day ' + s + ' (' + m + ' ' + y + ')')
    if not os.path.exists(fileName):
        print '\nNo stories on this day!'
    return fileName

def random():                                                   # Useful only when you have a lot of stories (obviously)
    for i in range(128):                                        # 128 rounds of pseudo-randomness!
        fileName = choice(os.listdir(loc))
    print 'Choosing a story...'
    temp(loc + fileName)

def diary():
    while True:
        if os.path.exists(loc + 'TEMP.tmp'):
            os.remove(loc + 'TEMP.tmp')
        try:
            choices = ('\n\tWhat do you wanna do?\n',
                " 1: Write today's story",
                " 2: Random story",
                " 3: View the story of someday",
                " 4. Write the story for someday you've missed")
            print '\n\t\t'.join(choices)
            if os.path.exists(ploc):
                print '\t\t 0: Sign out'
            else:
                print '\t\t 0: Sign in'
            choice = raw_input('\nChoice: ')
            ch = ['write()', 'random()', 'temp(day())', 'write(day())']
            if choice == '0':
                if os.path.exists(ploc):
                    os.remove(ploc)
                    print 'Login credentials removed!'
                else:
                    check()
                    print 'Login credentials have been saved locally!'
            else:
                try:
                    eval(ch[int(choice)-1])
                except Exception:
                    print '\nIllegal choice!'
            choice = raw_input('\nDo something again (y/n)? ')
            if choice is not 'y':
                break
        except KeyboardInterrupt:
            print '\nQuitting...'
            break
