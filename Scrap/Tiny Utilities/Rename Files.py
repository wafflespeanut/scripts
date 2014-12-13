import os,subprocess,eyed3

path="C:\\TEMP\\"

def renvid():           # To rename video files after watching
    for i in os.listdir(path):
        p=subprocess.Popen(["vlc.exe",path+i])      # Meh, I could've used os.startfile()
        print "\nOld name:",i; s=str(raw_input('New name: '))
        if s=='': continue
        elif s=='!': break
        try: os.rename(path+i,path+s)
        except WindowsError:
            raw_input('\n\tFile being used! Continue after closing...')
            os.rename(path+i,path+s)

def renum():            # To rename numbered ones
    for i in os.listdir(path):
        k=0
        if i[0] in '1234567890':
            while i[k] in '1234567890' or i[k] in ' -': k+=1
        os.rename(path+i,path+i[k:])

def renmp3():           # To rename MP3s based on their metadata
    for i in os.listdir(path):
        f=eyed3.load(path+i)
        os.rename(path+i,path+f.tag.title+'.mp3')
