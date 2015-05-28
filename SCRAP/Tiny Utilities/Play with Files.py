import os, subprocess, eyed3, shutil, random

def rfile(drive = 'H:\\'):                  # Random walk files to open something!
    nodes = [stuff for stuff in os.listdir(drive) if stuff not in ('$RECYCE.BIN', 'System Volume Information', 'RECYCLER')]
    path = drive
    while True:
        dirName = random.choice(nodes)
        path += dirName
        if os.path.isfile(path):
            os.startfile(path)
            break
        else:
            path += '\\'
            nodes = os.listdir(path)

path = "C:\\TEMP\\OST\\"

def ren(path = path):                       # Rename video files after watching
    for File in os.listdir(path):
        proc = subprocess.Popen(["vlc.exe", path + File])      # os.startfile() could be used for opening all files!
        print "\nOld name:", File
            name = str(raw_input('New name:'))
        if name == '':
            continue
        elif name == '!':
            break
        while True:
            try:
                os.rename(path + File, path + name)
                break
            except WindowsError:
                raw_input('\n\tFile being used! Continue after closing...')
                continue

def num(path = path):                       # Rename numbered ones
    for File in os.listdir(path):
        k = 0
        if File[0] in '1234567890':
            while File[k] in '1234567890' or File[k] in ' -':
                k += 1
        os.rename(path + File, path + File[k:])

def mp3(path = path):                       # Rename MP3s based on their title
    for File in os.listdir(path):
        if not 'mp3' in File:
            continue
        File = eyed3.load(path + File)
        title = raw_input('Current title: % s\n[Enter] to use the current metadata, or type a new one:\n' % (f.tag.title))
        if title == '':
            title = File.tag.title
        else:
            File.tag.title = unicode(title)
            File.tag.save()
        os.rename(path + File, path + title + '.mp3')

src = "D:\\parts\\"
dest = "J:\\Other\\TEMP\\parts\\"

def move(src = src, dest = dest, s = '.jpg'):       # Move files!
    for File in os.listdir(src):
        if not os.path.exists(dest):
            os.mkdir(dest)
        if s in File:
            shutil.move(src + File, dest + File)          # os.rename() can be used only for moving within the same drives
