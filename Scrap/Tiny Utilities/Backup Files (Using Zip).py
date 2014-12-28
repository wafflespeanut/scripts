from os import *
from time import strftime

src="C:\\"; tar="C:\\Backup\\"

def backup(src,tar):      # Making use of GnuWin32 Zip 3.0
    if not path.exists(tar): mkdir(tar)
    today=strftime('%Y')+'-'+strftime('%m')+'-'+strftime('%d'); today=tar+sep+today
    u=raw_input('Add a description: ')
    now=strftime('%H')+'-'+strftime('%M')+'-'+strftime('%S')+'-'+'_'.join(u.split(' '))
    zipped=today+sep+now+'.zip'
    if not path.exists(today): mkdir(today); print "First Backup today!"
    else: print "You already have a backup!"
    cmd="zip -q -r {0} {1}".format(zipped,''.join(src))
    print "Zip command:",cmd; print "\nRunning..."
    if not system(cmd): print '\nSuccessfully backed up to',zipped
    else: print '\nBackup FAILED!'
    print "Press <Enter> to quit..."
    raw_input()
