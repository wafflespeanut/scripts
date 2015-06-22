import subprocess as sub
import os

default = '"C:\Program Files (x86)\MKVToolNix\mkvmerge.exe" -o "%s" "--language" \
        "0:eng" "--default-track" "0:yes" "--forced-track" "0:no" "--language" \
        "1:eng" "--default-track" "1:yes" "--forced-track" "1:no" "-a" "1" "-d" \
        "0" "-S" "-T" "--no-global-tags" "--no-chapters" "(" "%s" ")" "--language" \
        "0:eng" "--default-track" "0:yes" "--forced-track" "0:no" "-s" "0" "-D" \
        "-A" "-T" "--no-global-tags" "--no-chapters" "(" "%s" ")" "--track-order" \
        "0:0,0:1,1:0"'          # Output filename; Input filename; Input SRT

path = "C:\\TEMP\\"

def mkv(path = path, ext = '.mkv'):
    if not os.path.exists(path + 'Converted'):
        os.mkdir(path + 'Converted')
    for File in os.listdir(path):
        if ext in File:
            name = File.split('.')[0]
            inFile = path + name + ext
            outFile = path + 'Converted' + os.sep + name + '.mkv'
            if not os.path.exists(path + name + '.srt'):
                print "SRT doesn't exists! Stopping conversion of %s" % File
                break
            srt = path + name + '.srt'
            process = sub.Popen(default % (outFile, inFile, srt), stderr = sub.STDOUT, stdout = sub.PIPE)
            output, errors = process.communicate()
