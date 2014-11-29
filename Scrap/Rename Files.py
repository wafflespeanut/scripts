import os, subprocess

path="H:\\TV Shows\\"

def ren():          # To rename video files after watching
    for i in os.listdir(path):
        p=subprocess.Popen(["vlc.exe",path+i])
        print "\nOld name:",i; s=str(raw_input('New name: '))
        if s=='': continue
        elif s=='!': break
        try: os.rename(path+i,path+s)
        except WindowsError:
            raw_input('\n\tFile being used! Continue after closing...')
            os.rename(path+i,path+s)

def num():          # To rename numbered ones
    for i in os.listdir(path):
        k=0
        if i[0] in '1234567890':
            while i[k] in '1234567890' or i[k] in ' -': k+=1
        os.rename(path+i,path+i[k:])
