import os,subprocess,eyed3,shutil

path="C:\\TEMP\\"

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

def mp3():           # To rename MP3s based on their metadata
    for i in os.listdir(path):
        f=eyed3.load(path+i)
        os.rename(path+i,path+f.tag.title+'.mp3')

src="D:\\parts\\"
dest="J:\\Other\\TEMP\\parts\\"

def move(s):             # To move files!
    for i in os.listdir(src):
        if not os.path.exists(dest): os.mkdir(dest)
        if s in i: shutil.move(src+i,dest+i)        # os.rename() can be used only for moving within the same drives
