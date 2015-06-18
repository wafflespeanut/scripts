from os import *
from time import strftime as stime

src = "C:\\Stuff"
tar = "C:\\Backup\\"

def backup(src, tar):               # Making use of GnuWin32 Zip 3.0
    if not path.exists(tar):
        mkdir(tar)
    today = stime('%Y') + '-' + stime('%m') + '-' + stime('%d')
    today = tar + sep + today
    subject = raw_input('Add a subject: ')
    now = stime('%H') + '-' + stime('%M') + '-' + stime('%S') + '-' + '_'.join(subject.split(' '))
    zipped = today + sep + now + '.zip'
    if not path.exists(today):
        mkdir(today)
        print "First Backup today!"
    else:
        print "You already have a backup!"
    cmd = "zip -q -r {0} {1}".format(zipped, ''.join(src))
    print "Zip command:", cmd, "\nRunning..."
    if not system(cmd):
        print '\nSuccessfully backed up to', zipped
    else:
        print '\nBackup FAILED!'
    raw_input("Press <Enter> to quit...")
