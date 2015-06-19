import os, sys, subprocess
from time import sleep
from time import strftime as time
from datetime import datetime, timedelta
from random import choice
from hashlib import md5

# Modified for my Ubuntu/Windows-8 dual-boot...

if '/bin' in os.path.defpath:
    ploc = '/media/Windows/Users/Waffles Crazy Peanut/AppData/Local/SYSTEM.DAT'
    loc = '/media/Windows/Users/Waffles Crazy Peanut/Desktop/Dropbox/Diary/'
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

def startfile(File):                                            # Platform-independent viewer
    if sys.platform == "win32":
        subprocess.Popen(["notepad", File])
    else:
        app = "open" if sys.platform is "darwin" else "xdg-open"
        subprocess.call([app, File])

def hexed(text):                                                # Hexing function
    return map(lambda i:
        format(ord(i), '02x'), list(text))

def hashed(stuff):                                              # MD5 hashing
    hashObject = md5()
    hashObject.update(stuff)
    return hashObject.hexdigest()

def char(text):                                                 # Hex-decoding function
    split = [text[i:i+2] for i in range(0, len(text), 2)]
    try:
        return ''.join(i.decode('hex') for i in split)
    except TypeError:
        return None

def shift(text, amount):                                         # Shifts the ASCII value of the chars (Vigenere cipher? Yep!)
    try:
        shiftedText = ''
        for i, ch in enumerate(text):
            shiftChar = ord(ch) + amount
            while shiftChar > 255:
                shiftChar -= 255
            shiftedText += chr(shiftChar)
    except TypeError:
        return None
    return shiftedText

def zombify(mode, data, key):                                   # Linking helper function
    hexedKey = ''.join(hexed(key))
    text = data
    if mode == 'e':
        text = ''.join(hexed(data))
        for ch in hexedKey:
            text = shift(text, ord(ch))
        return text
    elif mode in ('d', 'rw'):
        for ch in hexedKey:
            text = shift(text, 255 - ord(ch))
        return char(text)

def temp(File, key = None):                                     # Uses default notepad to view the 'temporary' story
    if File == None:
        return None
    if protect(File, 'd', key):
        startfile(loc + 'TEMP.tmp')
        sleep(2)
        os.remove(loc + 'TEMP.tmp')

def check():                                                    # Allows password to be stored locally
    if not os.path.exists(ploc):
        try:
            while True:
                key = raw_input('\nEnter password: ')
                if len(key) < 8:
                    print 'Choose a strong password! (at least 8 chars)'
                    continue
                if raw_input('Re-enter password: ') == key:
                    break
                else:
                    print "\nPasswords don't match!"
            for i in range(10):                                 # Nothing too serious, it just hexes the thing 10 times!
                key = ''.join(hexed(key))
            with open(ploc, 'w') as file:
                file.writelines(key)
            print 'Login credentials have been saved locally!'
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

def protect(path, mode, key = None):                            # A simple method which shifts and turns it to hex!
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
        return 0
    File = (path if mode in ('e', 'rw') else (loc + 'TEMP.tmp') if mode == 'd' else None)
    if not File:
        print 'Wrong mode!'
        return None
    with open(File, 'w') as file:
        file.writelines(data)
    return key

def write(File = None):                                         # Does the dirty writing job
    key = None
    if not File:
        File = loc + hashed('Day ' + time('%d') + ' (' + months[time('%m')] + ' ' + time('%Y') + ')')
    if os.path.exists(File) and os.path.getsize(File) >= 16:
        print '\nFile already exists! Appending to current file...'
        while not key:
            key = protect(File, 'rw')
            if key == 0:
                return None
            if not key:
                print 'A password is required to append to an existing file. Running sequence again...'
    elif os.path.exists(File):
        os.remove(File)
    timestamp = str(datetime.now()).split('.')[0].split(' ')
    data = ['[' + timestamp[0] + '] ' + timestamp[1] + '\n']
    try:
        stuff = raw_input('''\nStart writing... (Press Ctrl+C when you're done!)\n\n\t''')
        data.append(stuff)
    except KeyboardInterrupt:
        print 'Nothing written! Quitting...'
        protect(File, 'e', key)
        return None
    while True:
        try:
            stuff = raw_input('\t')                             # Auto-tabbing
            data.append(stuff)
        except KeyboardInterrupt:
            break
    with open(File, 'a') as file:
        file.writelines('\n\t'.join(data) + '\n\n')
    while True:
        key = protect(File, 'e', key)
        if not key:
            print "\nPlease don't interrupt! Your story is insecure! Running sequence again..."
        else:
            break
    choice = raw_input('\nSuccessfully written to file! Do you wanna see it (y/n)? ')
    if choice == 'y':
        temp(File, key)

def hashDate(year = None, month = None, day = None):            # Return a path based on (day, month, year) input
    while True:
        try:
            if not year:
                year = raw_input('\nYear: ')
            if not month:
                month = raw_input('\nMonth: ')
            if not day:
                day = raw_input('\nDay: ')
            date = str(datetime(int(year), int(month), int(day)).date()).split('-')
            if date:
                year = date[0]
                month = months[date[1]]
                day = date[2]
                break
        except Exception as err:
            print "An error occurred:", err
            year, month, day = None, None, None
            continue
    fileName = loc + hashed('Day ' + day + ' (' + month + ' ' + year + ')')
    if not os.path.exists(fileName):
        print '\nNo stories on {} {}, {}.'.format(month, day, year)
        return None
    return fileName

def random():                                                   # Useful only when you have a lot of stories (obviously)
    for i in range(128):                                        # 128 rounds of pseudo-randomness!
        fileName = choice(os.listdir(loc))
    print 'Choosing a story...'
    temp(loc + fileName)

def search():                                                   # Quite an interesting function for searching
    if os.path.exists(ploc):
        k = raw_input('Enter your password to continue: ')
        if not k == check():
            print '\n\tWrong password!'
            return None
    else:
        print 'You must sign-in to continue...'                 # Just for security...
        key = check()
    word = raw_input("Enter a word: ")
    choice = int(raw_input("\n\t1. Search everything!\n\t2. Search between two dates\n\nChoice: "))
    if choice == 1:
        d1 = datetime(2014, 12, 13)                             # Happy Birthday, Diary!
        d2 = datetime.now()
    while choice == 2:
        try:
            print '\nEnter dates in the form YYYY-MM-DD (Mind you, with hyphen!)'
            d1 = datetime.strptime(raw_input('Start date: '), '%Y-%m-%d')
            d2 = raw_input("End date (Press <Enter> for today's date): ")
            if not d2:
                d2 = datetime.now()
            else:
                d2 = datetime.strptime(d2, '%Y-%m-%d')
        except ValueError:
            print '\nOops! Error in input. Try again...'
            continue
        break
    delta = (d2 - d1).days
    print '\nDecrypting %d stories sequentially...' % delta     # Exhaustive process requires a low-level language
    print '\nSit back & relax... (May take some time)\n'        # That's why I'm learning Rust by translating this...
    fileData = [], [], []
    displayProg = 0
    printed = False
    for i in range(delta):
        d = d1 + timedelta(days = i)
        File = hashDate(d.year, d.month, d.day)
        if File == None:
            continue
        progress = int((float(i + 1) / delta) * 100)
        if progress is not displayProg:
            displayProg = progress
            printed = False
        occurred = 0
        if protect(File, 'd'):
            with open(loc + 'TEMP.tmp', 'r') as file:
                data = file.readlines()
            occurred = ''.join(data).count(word)
        else:
            print 'Cannot decrypt story! Skipping...'
            continue
        if occurred:
            fileData[0].append(i)
            fileData[1].append(occurred)
            fileData[2].append(File)
        if not printed:
            print 'Progress: %d%s \t(Found: %d)' % (displayProg, '%', sum(fileData[1]))
            printed = True
    r1 = str(d1.date()).split('-')
    r2 = str(d2.date()).split('-')
    ranges = months[r1[1]], r1[2], r1[0], months[r2[1]], r2[2], r2[0]
    print "\nSearch results from %s %s, %s to %s %s, %s" % ranges
    if fileData[1]:
        print "\nStories on these days have the word '%s' in them...\n" % word
    else:
        print '\nBad luck! Nothing...'
    for i, delta in enumerate(fileData[0]):
        d = str(datetime(d1.year, d1.month, d1.day).date() + timedelta(days = delta)).split('-')
        print '%d. %s %s, %s' % (i + 1, months[d[1]], d[2], d[0])
    print '\nFound %d occurrences in %d stories!' % (sum(fileData[1]), len(fileData[0]))
    os.remove(loc + 'TEMP.tmp')
    while fileData[2]:
        try:
            ch = int(raw_input('Enter a number to open the corresponding story: '))
            temp(fileData[2][ch - 1])
        except Exception:
            print '\nOops! Bad input...\n'

def diary():
    choice = 'y'
    while choice is 'y':
        if os.path.exists(loc + 'TEMP.tmp'):
            os.remove(loc + 'TEMP.tmp')
        try:
            choices = ('\n\tWhat do you wanna do?\n',
                " 1: Write today's story",
                " 2: Random story",
                " 3: View the story of someday",
                " 4. Write the story for someday you've missed",
                " 5. Search your stories")
            print '\n\t\t'.join(choices)
            if os.path.exists(ploc):
                print '\t\t 0: Sign out'
            else:
                print '\t\t 0: Sign in'
            choice = raw_input('\nChoice: ')
            ch = ['write()', 'random()', 'temp(hashDate())', 'write(hashDate())', 'search()']
            if choice == '0':
                if os.path.exists(ploc):
                    os.remove(ploc)
                    print 'Login credentials removed!'
                else:
                    print "\n[WARNING] Anyone will be able to see your story if you don't sign out!"
                    check()
            else:
                try:
                    eval(ch[int(choice)-1])
                except Exception:
                    print '\nAh, something bad has happened! Did you do it?'
            choice = raw_input('\nDo something again (y/n)? ')
        except KeyboardInterrupt:
            choice = raw_input('\nInterrupted! Do something again (y/n)? ')
