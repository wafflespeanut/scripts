import os,subprocess,eyed3,shutil,random

def rfile(drive='H:\\'):            # Random walk files to open something! (Got bored)
    k=[i for i in os.listdir(drive) if i not in ('$RECYCLE.BIN','System Volume Information','RECYCLER')]; s=drive
    while True:
        c=random.choice(k); s+=c
        if os.path.isfile(s): os.startfile(s); break
        else: s+='\\'; k=os.listdir(s)

path="C:\\TEMP\\OST\\"

def ren():           # To rename video files after watching
    for i in os.listdir(path):
        p=subprocess.Popen(["vlc.exe",path+i])      # os.startfile() could be used for opening all files!
        print "\nOld name:",i; s=str(raw_input('New name: '))
        if s=='': continue
        elif s=='!': break
        while True:
            try: os.rename(path+i,path+s); break
            except WindowsError:
                raw_input('\n\tFile being used! Continue after closing...'); continue

def num():            # To rename numbered ones
    for i in os.listdir(path):
        k=0
        if i[0] in '1234567890':
            while i[k] in '1234567890' or i[k] in ' -': k+=1
        os.rename(path+i,path+i[k:])

def mp3():           # To rename MP3s based on their title
    for i in os.listdir(path):
        if not 'mp3' in i: continue
        f=eyed3.load(path+i)
        s=raw_input('Current title: %s\n[Enter] to use the current metadata, or type a new one:\n'%(f.tag.title))
        if s=='': s=f.tag.title
        else: f.tag.title=unicode(s); f.tag.save()
        os.rename(path+i,path+s+'.mp3')

src="D:\\parts\\"
dest="J:\\Other\\TEMP\\parts\\"

def move(s):             # To move files!
    for i in os.listdir(src):
        if not os.path.exists(dest): os.mkdir(dest)
        if s in i: shutil.move(src+i,dest+i)        # os.rename() can be used only for moving within the same drives
