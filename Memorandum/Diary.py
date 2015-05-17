import os,subprocess
from time import strftime as time
from time import sleep
from random import choice

# Modified for my Ubuntu/Windows-8 dual-boot...

if '/bin' in os.path.defpath:
    ploc='/media/'+os.path.expanduser('~').split('/')[-1]+'/Local Disk/Users/Waffles Crazy Peanut/AppData/Local/SYSTEM.DAT'
    loc='/media/'+os.path.expanduser('~').split('/')[-1]+'/Local Disk/Users/Waffles Crazy Peanut/Desktop/Dropbox/Diary/'
else:
    ploc=os.path.expanduser('~')+'\\AppData\\Local\\SYSTEM.DAT'         # Password location
    loc=os.path.expanduser('~')+'\\Desktop\\Dropbox\\Diary - Copy\\'           # Storage location

months={'11':'November','10':'October','12':'December','01':'January','03':'March','02':'February','05':'May','04':'April','07':'July','06':'June','09':'September','08':'August'}

def hexed(key):             # Hexing function
    pas=list(key)
    for i,j in enumerate(pas): pas[i]=format(ord(pas[i]),'02x')
    return pas

def hashed(stuff,bits=32,rounds=128):        # Hashing a hexed string with specified rounds
    pad=bits-len(stuff)%bits            # Padding is solely for fun!
    if not pad/10: pad='0'+pad
    t=''.join(hexed(stuff))+str(pad)*pad
    for i in range(rounds): t=hash(str(t))
    return str(abs(t))

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

def zombify(ch,data,key):           # Linking helper function
    k=''.join(hexed(key)); p=data
    if ch=='e':
        p=''.join(hexed(data))
        for i in k: p=shift(p,ord(i))
        return p
    elif ch=='d':
        for i in k: p=shift(p,255-ord(i))
        return char(p)

def temp(File,key=None):            # Uses default notepad to view stuff
    if File==None: return None
    if protect(File,'d',key):
        subprocess.Popen(["notepad",loc+'TEMP.tmp'])
        sleep(2); os.remove(loc+'TEMP.tmp')

def check():                        # Allows password to be stored locally (Nothing too serious, it just hexes the thing 10 times!)
    if not os.path.exists(ploc):
        try:
            k1=True; k2=False
            while True:
                k1=raw_input('\nEnter password: ')
                while len(k1)<8: k1=raw_input('\nEnter password of at least 8 chars: ')
                k2=raw_input('Re-enter password: ')
                if k1==k2: break
                else: print "\nPasswords don't match!\n"
            key=k1=k2
            for i in range(10): key=''.join(hexed(key))
            with open(ploc,'w') as file: file.writelines(key)
        except KeyboardInterrupt: print 'Login credentials failed!'; return None
    else:
        with open(ploc,'r') as file: key=file.readlines()
        if key: key=key[0]
        else: return None
        for i in range(10): key=char(key)
    return key

def protect(path,ch,key=None):      # A simple method which shifts and turns it to hex!
    if os.path.exists(ploc): key=check()
    try:
        if not key: key=raw_input('\nEnter password for your story: ')
        while len(key)<8: key=raw_input('\nEnter password of at least 8 chars: ')
    except KeyboardInterrupt: return False
    with open(path,'r') as file: data=file.readlines()
    if len(data)==0: print 'Nothing in file!'; return None
    try:
        for i in range(len(data)):      # The '\r\n' thing is for newline char in Ubuntu
            if data[i]=='\n' or data[i]=='\r\n': i+=1; continue
            if data[i][-2:]=='\r\n': data[i]=zombify(ch,str(data[i][:-2]),key); c=True
            elif data[i][-1]=='\n': data[i]=zombify(ch,str(data[i][:-1]),key); c=True
            else: data[i]=zombify(ch,str(data[i]),key); c=False
            if c and 'bin' in ploc: data[i]+='\r\n'
            elif c: data[i]+='\n'
    except TypeError: print '\n\tWrong password!'; return None
    if ch=='e':
        with open(path,'w') as file: file.writelines(data)
    elif ch=='d':
        with open(loc+'TEMP.tmp','w') as file: file.writelines(data)
    return key

def write(File=None):      # Does all the dirty job
    key=None
    if not File: File=hashed('Day '+time('%d')+' ('+months[time('%m')]+' '+time('%Y')+')')
    if os.path.exists(File) and os.path.getsize(File)!=0:
        print '\nFile already exists! Appending to current file...'
        while not key:
            key=protect(File,'d')
            if not key: print 'A password is required to append to an existing file. Running sequence again...'
        with open(loc+'TEMP.tmp','r') as file: data=file.readlines()
        with open(File,'w') as file: file.writelines(data)
        os.remove(loc+'TEMP.tmp')
    elif os.path.exists(File): os.remove(File)
    f=open(File,'a')
    a=['['+time('%Y')+'-'+time('%m')+'-'+time('%d')+']'+' '+time('%H')+':'+time('%M')+':'+time('%S')+'\n']
    try: s=raw_input('''\nStart writing... (Press Ctrl+C when you're done!)\n\n\t'''); a.append('\t'+s)
    except KeyboardInterrupt: print 'Nothing written! Quitting...'; protect(File,'e',key); return None
    while True:
        try: s=raw_input(); a.append(s)
        except KeyboardInterrupt: break
    f.write('\n'.join(a)+'\n\n'); f.close(); k=None
    if key: k=key; key=None
    while not key:
        if k: key=k
        key=protect(File,'e',key)
        if not key: print "\nPlease don't interrupt! Your story is insecure! Running sequence again..."
    s=raw_input('\nSuccessfully written to file! Do you wanna see it (y/n)? ')
    if s=='y': temp(File,key)

def day():              # Return a path based on (day,month,year) input
    while True:
        y=raw_input('\nYear: ')
        if len(y)==4: break
    while True:
        s=raw_input('\nMonth: ')
        if s in months: m=months[s]; break
        elif '0'+s in months: m=months['0'+s]; break
    while True:
        s=raw_input('\nDay: ')
        if len(s)==1: s='0'+s
        if int(s)<32: break
    f=hashed('Day '+s+' ('+m+' '+y+')')
    if not os.path.exists(f): print '\nNo stories on this day!'
    return f

def random():       # Useful only when you have a lot of stories
    for i in range(128):        # Just to approach pure randomness instead of pseudo-randomness
        y=choice(os.listdir(loc)); m=choice(os.listdir(loc+y))
        d=choice(os.listdir(loc+y+os.sep+m)); f=loc+os.sep+y+os.sep+m+os.sep+d
    print 'Choosing your story from '+d+'...'; temp(f)

def diary():
    while True:
        if os.path.exists(loc+'TEMP.tmp'): os.remove(loc+'TEMP.tmp')
        try:
            print '\n\tWhat do you wanna do?',"\n\n\t\t1: Write today's story","\n\t\t2: Random story","\n\t\t3: View the story of someday","\n\t\t4. Write the story for someday you've missed"
            if os.path.exists(ploc): print '\t\t0: Sign out'
            else: print '\t\t0: Sign in'
            s=raw_input('\nChoice: ')
            ch=['write()','random()','temp(day())','write(day())']
            if s=='0':
                if os.path.exists(ploc): os.remove(ploc); print 'Login credentials removed!'
                else: check(); print 'Login credentials have been saved locally!'
            try: eval(ch[int(s)-1])
            except Exception: print '\nIllegal choice!'
            s=raw_input('\nDo something again (y/n)? ')
            if s!='y': break
        except KeyboardInterrupt: print '\nQuitting...'; break
