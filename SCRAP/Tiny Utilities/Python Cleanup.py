import os

path="C:\\Users\\Waffles Crazy Peanut\\Desktop\\Diary.py"

def search(path=path,ext='py'):             # For listing all those .py files
    fileList=[]
    for root,dirs,files in os.walk(path):
        temp=[root+'\\'+f for f in files if f[-len(ext):]==ext]
        fileList.extend(temp)
    return fileList

def symbols(line):
    if line=='\n': return '\n'
    punc=['"',"'"]; i=0; copy=list(line); sym='+-/*=%<>^!|&'
    ch=''.join(line.split())[0]; tab=line.index(ch)
    
    def string(index):                  # Skip strings
        ch=copy[index]; i=index+1
        if line[index:index+3]=="'''": return line.index("'''")
        while copy[i] is not ch:
            if copy[i]=='\\': i+=1
            i+=1
        return i

    def math(stuff,index):              # Spaced symbols
        i=index; copy=stuff[:]
        if copy[i-1] is not ' ': copy[i]=' '+copy[i]
        if copy[i+1] is '=' and copy[i+2] is not ' ': copy[i+1]='= '; i+=1
        elif copy[i+1] is not ' ': copy[i]+=' '
        return copy,i

    while i<len(copy):
        if copy[i] in ['\n','#']: break
        if copy[i] in punc: i=string(i)
        elif copy[i]==',' and copy[i+1] is not ' ': copy[i]+=' '
        elif copy[i]=='{':              # Grouped dicts
            sp=tab+4; copy[i]+='\n'+sp*' '
            while True:
                i+=1
                if copy[i] in punc: i=string(i)
                elif copy[i] in sym: copy,i = math(copy,i)
                elif copy[i] is ',': copy[i]+='\n'+sp*' '
                elif copy[i] is ':' and copy[i+1] is not ' ': copy[i]+=' '
                elif copy[i] is '}':
                    copy[i]='\n'+tab*' '+'}'; break
        elif copy[i]=='[':              # Spaced lists
            items=''
            while copy[i] is not ']':
                i+=1
                if copy[i] in punc: i=string(i)
                elif copy[i] in sym: copy,i = math(copy,i)
                elif copy[i]==',' and copy[i+1] is not ' ': copy[i]+=' '
                items+=copy[i]
        elif copy[i]==':':              # Colons with newlines
            if copy[i+1]=='\n': i+=1; continue
            else: tab+=4
            if copy[i+1]==' ': copy[i+1]='\n'+tab*' '
            elif copy[i+1] is not '\n': copy[i]=':\n'+tab*' '
        elif copy[i] in sym: copy,i = math(copy,i)
        elif copy[i]==';':              # Abandon semicolons!
            copy[i]='\n'+tab*' '; i+=1
            while copy[i]==' ': copy[i]=''; i+=1
        i+=1
    return ''.join(copy)

def cleanup(File):
    with open(File,'r') as file: data=file.readlines()
    return data
    from time import sleep
    for i in data:
        print symbols(i); sleep(1)

a=cleanup(path)             # Only for testing purposes...
while True:
    print symbols(a[int(raw_input())])
