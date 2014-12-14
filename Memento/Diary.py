import os,subprocess
from time import strftime as time

loc='C:\\Users\\Waffles Crazy Peanut\\Desktop\\Dropbox\\Diary\\'        # Storage location
months={'11':'November','10':'October','12':'December','1':'January','3':'March','2':'February','5':'May','4':'April','7':'July','6':'June','9':'September','8':'August'}

# Random stories & viewing stories (with info) are on the way...

def hexed(key):             # Hexing function
    pas=list(key)
    for i,j in enumerate(pas): pas[i]=format(ord(pas[i]),'02x')
    return pas

def char(key):              # Hex-decoding function
    pas=[key[i:i+2] for i in range(0,len(key),2)]
    for i,j in enumerate(pas):
        try: pas[i]=pas[i].decode("hex")
        except TypeError: return None
    return ''.join(pas)

def shift(text,shift):      # Shifts the ASCII value of the chars (reversible)
    try:
        new=''
        for i,j in enumerate(text):
            m=ord(j)+shift
            while m>255: m-=255
            new+=chr(m)
    except TypeError: return None
    return new

def zombify(ch,data,key):
    k=''.join(hexed(key))
    if ch=='e':
        p=''.join(hexed(data))
        for i in k: p=shift(p,ord(i)); return p
    elif ch=='d':
        p=data
        for i in k: p=shift(p,255-ord(i)); return char(p)

def temp(File):
    protect(File,'d'); subprocess.Popen(["notepad.exe",loc+'TEMP.tmp'])
    #os.remove(loc+'TEMP.tmp')

def protect(path,ch):              # A simple encryption which shifts and turns it to hex!
    try:
        key=raw_input('\nEnter password for your story: ')
        while len(key)<4: key=raw_input('\nEnter password of at least 4 chars: ')
    except KeyboardInterrupt: return False
    with open(path,'r') as file: data=file.readlines()
    if len(data)==0: print 'Nothing in file!'; return None
    for i in range(len(data)):
        if data[i]=='\n': i+=1; continue
        if data[i][-1]=='\n': data[i]=zombify(ch,str(data[i][:-1]),key); c=True
        else: data[i]=zombify(ch,str(data[i]),key); c=False
        if c: data[i]+='\n'
    if ch=='e':
        with open(path,'w') as file: file.writelines(data)
    elif ch=='d':
        with open(loc+'TEMP.tmp','w') as file: file.writelines(data)
    return True

def write():
    if not os.path.exists(loc+time('%Y')): os.mkdir(loc+time('%Y'))
    f=loc+time('%Y')+os.sep+months[time('%m')]+' ('+time('%Y')+')'
    if not os.path.exists(f): os.mkdir(f)
    File=f+os.sep+'Day '+time('%d')+' ('+months[time('%m')]+' '+time('%Y')+')'
    if os.path.exists(File):
        print '\nFile already exists! Password required!'
        while not protect(File,'d'): print 'A password is required to append to an existing file. Running sequence again...'
        with open(loc+'TEMP.tmp','r') as file: data=file.readlines()
        with open(File,'w') as file: file.writelines(data)
    os.remove(loc+'TEMP.tmp'); f=open(File,'a')
    a=['['+time('%Y')+'-'+time('%m')+'-'+time('%d')+']'+' '+time('%H')+':'+time('%M')+':'+time('%S')+'\n']
    try: s=raw_input('''\nStart writing... (Press Ctrl+C when you're done!)\n\n\t'''); a.append('\t'+s)
    except KeyboardInterrupt: print 'Nothing written! Quitting...'; return None
    while True:
        try: s=raw_input(); a.append(s)
        except KeyboardInterrupt: break
    f.write('\n'.join(a)+'\n\n'); f.close()
    while not protect(File,'e'):
        print "\nPlease don't interrupt! Your story is insecure! Running sequence again..."
    s=raw_input('\nSuccessfully written to file! Do you wanna see it (y/n)? ')
    if s=='y': temp(File)

def view():
    y=raw_input('\nYear: ')
    if not os.path.exists(loc+y): print '\nNo stories on this year...'; return None
    while True:
        try: m=months[raw_input('\nMonth: ')]; break
        except KeyError: print 'Enter a valid month!'
    if not os.path.exists(loc+y+os.sep+m+' ('+y+')'): print '\nNo stories on this month...'; return None
    d='Day '+raw_input('\nDay: ')+' ('+m+' '+y+')'; f=loc+y+os.sep+m+' ('+y+')'+os.sep+d
    if not os.path.exists(f): print '\nNo stories this day...'; return None
    else: temp(f)

def diary():
    s=raw_input("\n\tWhat do you wanna do?\n\n\t\t1. Write today's story\n\t\t2. Random story\n\t\t3. View the story of someday\n\nChoice: ")
    if s=='1': write()
    elif s=='2': print '\nNot yet implemented - Will be done soon...'
    elif s=='3': view()
    else: print '\nIllegal choice! Quitting...'
