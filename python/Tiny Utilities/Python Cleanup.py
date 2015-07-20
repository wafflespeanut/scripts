import os

path = os.path.expanduser('~/Desktop/Github/scripts/python/Project Euler')

# A script to cleanup my old code (works quite nicely only for totally shitty code!)
# May screw your code if it's already clean (though I've never tried it)
# It works only on Windows!

def search(path, ext = 'py'):                           # For listing all those .py files
    fileList = []
    for root, dirs, files in os.walk(path):
        temp = [root + os.sep + f for f in files if f[-len(ext):] == ext]
        fileList.extend(temp)
    return sorted(fileList)

def symbols(line):
    firstChar = ''.join(line.split())
    if firstChar:
        tab = line.index(firstChar[0])
    else:
        return '\n'
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
                    ch[ - 1] = ''
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
        if copy[i] in ['\n', '#']:
            break

        if copy[i] in punc:
            i = string(i)

        elif copy[i] == ',' and copy[i + 1] is not ' ':
            copy[i] += ' '

        elif copy[i] == '{' and copy[i + 1] is not '\n':      # Grouped dicts
            sp = tab + 4
            copy[i] += '\n' + sp * ' '
            while True:
                i += 1
                if copy[i] in punc:
                    i = string(i)
                elif copy[i] in sym:
                    copy, i = math(copy, i)
                elif copy[i] is ',':
                    copy[i] += '\n' + sp * ' '
                elif copy[i] is ':' and copy[i + 1] is not ' ':
                        copy[i] += ' '
                elif copy[i] is '}':
                    copy[i] = '\n' + tab * ' ' + '}\n'
                    break

        elif copy[i] == '[':                            # Spaced lists
            items = ''
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
            if copy[i + 1] == '\n':
                i += 1
                continue
            elif line[i + 1:].split()[0] is '#':
                break
            else:
                tab += 4
            if copy[i + 1] == ' ':
                copy[i + 1] = '\n' + tab * ' '
            elif copy[i + 1] is not '\n':
                copy[i] = ':\n' + tab * ' '

        elif copy[i] in sym:
            copy, i = math(copy, i)

        elif copy[i] == ';':                            # Abandon semicolons!
            copy[i] = '\n' + tab * ' '
            i += 1
            while copy[i] == ' ':
                copy[i] = ''
                i += 1
        i += 1
    return ''.join(copy)

def cleanup(path = path, index = 0):                    # The index is just to start from previously interrupted file
    count = 0
    for File in search(path):
        try:
            if index and count < index:
                count += 1
                continue
            print 'Cleaning up', File, '...\n'
            with open(File, 'r') as file:
                data = file.readlines()
            for l in range(len(data)):
                data[l] = symbols(data[l])
            print '<----- START OF FILE ----->\n', ''.join(data), '\n<----- END OF FILE ----->'
            if raw_input('Continue writing to file (y/n)? ') == 'y':
                with open(File, 'w') as file:
                    file.writelines(data)
                count += 1
                os.startfile(File)
                if raw_input('Continue (y/n)? ') is not 'y':
                    break
        except (KeyboardInterrupt, Exception):
            print '\n\nInterrupted at File %s! (Line: %s)' % (count, l)
            break
