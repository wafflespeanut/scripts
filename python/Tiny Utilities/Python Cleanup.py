import os, sys, subprocess

path = os.path.expanduser('~/Desktop/Github/scripts/python/Project Euler')

# A script to cleanup my old code (works quite nicely only for totally shitty code!)
# May screw your code if it's already clean (though I've never tried it)

def search(path, ext = '.py'):                           # For listing all those .py files
    fileList = []
    for root, dirs, files in os.walk(path):
        temp = [root + os.sep + f for f in files if f.endswith(ext)]
        fileList.extend(temp)
    return sorted(fileList)

def startFile(File):
    if sys.platform == 'win32':
        os.startfile(File)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, File])

def symbols(line):
    firstChar = ''.join(line.split())
    newline = (line[-2:] if line[-2:] == '\r\n' else line[-1])
    if firstChar:
        tab = line.index(firstChar[0])
    else:
        return newline
    i = 0
    punc = ['"', "'"]
    copy = list(line)
    sym = '+-/*=%<>^!|&'

    def string(x):                                      # Skip strings
        ch = copy[x]
        if line[x: x + 3] == "'''":
            return line[x + 3:].index("'''") + x + 6
        x += 1
        while copy[x] is not ch:
            if copy[x] == '\\':
                x += 1
            x += 1
        return x

    def math(stuff, index):                             # Spaced symbols
        i = index
        copy = stuff[:]

        def double(x):                                  # For **, +=, //, etc.
            ch = [' ', copy[x], copy[x + 1], ' ']
            if all([copy[x] in sym, copy[x + 1] in sym]):
                if copy[x - 1] is ' ':
                    ch[0] = ''
                if copy[x + 2] is ' ':
                    ch[-1] = ''
                return ''.join(ch)
            return False

        if double(i):
            copy[i], copy[i + 1] = double(i), ''
            i += 1
        elif copy[i - 1] is not ' ':
            copy[i] = ' ' + copy[i]
            if copy[i + 1] is not ' ':
                copy[i] += ' '
        return copy, i

    while i < len(copy):
        if copy[i] in list(newline) + ['#']:
            break

        if copy[i] in punc:
            i = string(i)

        elif copy[i] == ',' and copy[i + 1] is not ' ':
            copy[i] += ' '

        elif copy[i] == '{' and copy[i + 1] is not newline:      # Grouped dicts
            sp = tab + 4
            copy[i] += newline + sp * ' '
            while True:
                i += 1
                if copy[i] in punc:
                    i = string(i)
                elif copy[i] in sym:
                    copy, i = math(copy, i)
                elif copy[i] is ',':
                    copy[i] += newline + sp * ' '
                elif copy[i] is ':' and copy[i + 1] is not ' ':
                        copy[i] += ' '
                elif copy[i] is '}':
                    copy[i] = newline + tab * ' ' + '}' + newline
                    break

        elif copy[i] == '[':                            # Spaced lists
            items = ''
            if ']' not in line:
                i += 1
                continue
            while copy[i] is not ']':
                i += 1
                if copy[i] in punc:
                    i = string(i)
                elif copy[i] in sym:
                    copy, i = math(copy, i)
                elif copy[i] in [':', ','] and copy[i + 1] is not ' ':
                    copy[i] += ' '
                items += copy[i]

        elif copy[i] == ':':                            # Colons with newlines
            if copy[i + 1] in list(newline):
                i += 1
                continue
            elif line[i + 1:].split():
                if line[i + 1:].split()[0] == '#':
                    break
                else:
                    tab += 4
            if copy[i + 1] == ' ':
                copy[i + 1] = newline + tab * ' '
            elif copy[i + 1] is not newline:
                copy[i] = ':' + newline + tab * ' '

        elif copy[i] in sym:
            copy, i = math(copy, i)

        elif copy[i] == ';':                            # Abandon semicolons!
            copy[i] = newline + tab * ' '
            i += 1
            while copy[i] == ' ':
                copy[i] = ''
                i += 1
        i += 1
    return ''.join(copy)

def cleanup(path = path, index = 0):                    # The index is just to start from previously interrupted file
    toughLines, breaker = [], False
    files = search(path)
    while index < len(files):
        File = files[index]
        try:
            print 'Cleaning up', File, '...\n'
            with open(File, 'rb') as file:
                data = file.readlines()
            for l in range(len(data)):
                try:
                    data[l] = symbols(data[l])
                except IndexError:
                    toughLines.append(l)
            print '<----- START OF FILE %d ----->\n' % index
            print ''.join(data), '\n<----- END OF FILE %d ----->' % index
            if toughLines:
                print "\nCouldn't cleanup the following line(s):", toughLines
            if raw_input('Continue writing to file (y/n)? ') == 'y':
                with open(File, 'wb') as file:
                    file.writelines(data)
                startFile(File)
                if raw_input('Continue (y/n)? ') is not 'y':
                    index += 1
                    breaker = True
            else:
                breaker = True
            if breaker:
                print '\n\nInterrupted at File %s!' % (index)
                break
            index += 1
        except KeyboardInterrupt:
            print '\n\nInterrupted at File %s! (Line: %s)' % (index, l)
            break
