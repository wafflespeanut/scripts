import os,time

def backup(src,tar):      # Making use of GnuWin32 Zip 3.0
    zipped=tar+os.sep+time.strftime('%Y%m%d%H%M%S')+'.zip'
    if not os.path.exists(tar): os.mkdir(tar)
    cmd="zip -r {0} {1}".format(zipped,''.join(src))
    print "Zip command:",cmd
    print "\nRunning..."
    if not os.system(cmd): print '\nSuccessfully backed up to',zipped
    else: print '\nBackup FAILED!'
    print "Press <Enter> to quit..."
    raw_input()

