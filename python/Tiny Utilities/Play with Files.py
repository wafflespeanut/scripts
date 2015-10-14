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
    k = 0
    count = 0
    files = os.listdir(path)
    while count < len(files):
        for name in os.listdir(path):
            if 'E' + str(k+1).zfill(2) in name:
                count += 1
                ext = '.' + name.split('.')[-1]
                os.rename(path + name, path + 'Episode ' + str(k+1) + ext)
        k += 1

def mp3(path = path):                       # Rename MP3s based on their title
    for File in os.listdir(path):
        if File.endswith('.mp3'):
            continue
        loadFile = eyed3.load(path + File)
        newTitle = raw_input('Current title: % s\n[Enter] to use the current metadata, or type a new one:\n' \
                   % (loadFile.tag.title))
        if newTitle == '':
            newTitle = loadFile.tag.title
        else:
            loadFile.tag.title = unicode(newTitle)
            try:
                loadFile.tag.save()
            except Exception:
                print 'Couldn\'t save title!'
        os.rename(path + File, path + newTitle + '.mp3')

src = "D:\\parts\\"
dest = "J:\\Other\\TEMP\\parts\\"

def move(src = src, dest = dest, s = '.jpg'):       # Move files!
    for File in os.listdir(src):
        if not os.path.exists(dest):
            os.mkdir(dest)
        if s in File:
            shutil.move(src + File, dest + File)          # os.rename() can be used only for moving within the same drives
