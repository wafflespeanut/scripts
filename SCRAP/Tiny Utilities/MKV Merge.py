import subprocess as sub
import os

default = '"C:\Program Files (x86)\MKVToolNix\mkvmerge.exe" -o "%s" "--language" "0:eng" \
        "--default-track" "0:yes" "--forced-track" "0:no" "--display-dimensions" "0:1280x720" \
        "--language" "1:eng" "--default-track" "1:yes" "--forced-track" "1:no" "-a" "1" "-d" \
        "0" "-S" "-T" "--no-global-tags" "--no-chapters" "(" "%s" ")" "--language" "0:eng" \
        "--default-track" "0:yes" "--forced-track" "0:no" "-s" "0" "-D" "-A" "-T" \
        "--no-global-tags" "--no-chapters" "(" "%s" ")" "--track-order" "0:0,0:1,1:0"'
        # Output filename; Input filename; Input SRT

path = "C:\\TEMP\\Season 2\\"

def mkv(path = path):
    if not os.path.exists(path + 'Converted'):
        os.mkdir(path + 'Converted')
    i = 1
    while i <= len(os.listdir(path)) / 2:
        name = 'Episode ' + str(i) + '.mkv'
        inFile = path + name
        outFile = path + 'Converted' + os.sep + name
        srt = path + 'Episode ' + str(i) + '.srt'
        process = sub.Popen(default % (outFile, inFile, srt), stderr = sub.STDOUT, stdout = sub.PIPE)
        output, errors = process.communicate()
        print output
        i += 1
