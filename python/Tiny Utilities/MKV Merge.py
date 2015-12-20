execfile('Python Cleanup.py')
import subprocess as sub
import os, sys

program = 'C:\Program Files (x86)\MKVToolNix\mkvmerge.exe' if sys.platform == 'win32' else '/usr/bin/mkvmerge'
default = ['"%s"' % program, '-o "%s"',
           '"--language" "0:eng" "--default-track" "0:yes" "--forced-track" "0:no"',
           '"--language" "1:eng" "--default-track" "1:yes" "--forced-track" "1:no"',
           '"-a" "1" "-d" "0" "-S" "-T" "--no-global-tags" "--no-chapters" "(" "%s" ")"',
           '"--language" "0:eng" "--default-track" "0:yes" "--forced-track" "0:no"',
           '"-s" "0" "-D" "-A" "-T" "--no-global-tags" "--no-chapters" "(" "%s" ")"',
           '"--track-order" "0:0,0:1,1:0"']

path = "/media/Windows/TEMP/GOT"

def check_name(s):
    i = 0
    while i < len(s) - 3:
        if s[i] == 'S' and s[i + 3] == 'E':
            return int(s[(i + 1):(i + 3)]), int(s[(i + 4):(i + 6)])
        i += 1
    return None

def check_srt(file_name):
    with open(file_name, 'r') as file_data:
        for line in file_data.readlines():
            if 'http' in line or 'www' in line:
                return True
    return False

def mkv(path = path, ext = '.mp4'):
    new_path = os.path.join(path, 'Converted')
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for in_file in search(path, ext):
        name = os.path.basename(in_file)
        dir_name = os.path.dirname(in_file)
        try:
            s, e = check_name(name)
        except ValueError:
            print 'Cannot infer season & episode IDs for %s!' % in_file
            continue
        out_path = os.path.join(new_path, 'Season %d' % s)
        if not os.path.exists(out_path):
            os.mkdir(out_path)
        out_file = os.path.join(out_path, 'Episode %d.mkv' % e)
        try:
            srt = [f for f in os.listdir(dir_name) if f.endswith('.srt')]
            assert srt
            if len(srt) > 1:
                srt = [f for f in srt if 'eng' in f or 'Eng' in f]
            srt = os.path.join(dir_name, srt[0])
            if check_srt(srt):
                raw_input('SRT needs fix! (%s)\nContinue?' % srt)
        except AssertionError, IndexError:
            print 'SRT not found for %s!' % in_file
            continue
        command = ' '.join(default) % (out_file, in_file, srt)
        print 'Muxing ...\nCommand: %s\n' % command
        process = sub.Popen(command, stderr = sub.STDOUT, stdout = sub.PIPE, shell = True)
        output, errors = process.communicate()
