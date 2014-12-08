import os
from time import strftime

src="C:\\"; tar="C:\\Backup\\"

def backup(src,tar):      # Making use of GnuWin32 Zip 3.0
    if not os.path.exists(tar): os.mkdir(tar)
    today=strftime('%Y%m%d')
    today=today[:4]+'-'+today[4:6]+'-'+today[6:8]
    today=tar+os.sep+today; now=strftime('%H%M%S')
    u=raw_input('Add a description: ')
    now=now[:2]+'-'+now[2:4]+'-'+now[4:6]+'-'+'_'.join(u.split(' '))
    zipped=today+os.sep+now+'.zip'
    if not os.path.exists(today): os.mkdir(today); print "First Backup today!"
    else: print "You already have a backup!"
    cmd="zip -q -r {0} {1}".format(zipped,''.join(src))
    print "Zip command:",cmd
    print "\nRunning..."
    if not os.system(cmd): print '\nSuccessfully backed up to',zipped
    else: print '\nBackup FAILED!'
    print "Press <Enter> to quit..."
    raw_input()
