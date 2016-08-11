import inspect, os, sys

filename = inspect.getframeinfo(inspect.currentframe()).filename
exec_path = os.path.dirname(os.path.abspath(filename))
execfile(os.path.join(exec_path, 'helpers.py'))

PROGRAM = 'C:\Program Files (x86)\MKVToolNix\mkvmerge.exe' if sys.platform == 'win32' else '/usr/bin/mkvmerge'
DEFAULT = ['"%s"' % PROGRAM, '-o "%s"',
           '"--language" "0:eng" "--default-track" "0:yes" "--forced-track" "0:no"',
           '"--language" "1:eng" "--default-track" "1:yes" "--forced-track" "1:no"',
           '"-a" "1" "-d" "0" "-S" "-T" "--no-global-tags" "--no-chapters" "(" "%s" ")"',
           '"--language" "0:eng" "--default-track" "0:yes" "--forced-track" "0:no"',
           '"-s" "0" "-D" "-A" "-T" "--no-global-tags" "--no-chapters" "(" "%s" ")"',
           '"--track-order" "0:0,0:1,1:0"']

ALLOWED = ['mkv', 'mp4']
IN_PATH = "/media/Windows/TEMP/GOT"
OUT_PATH = os.path.join(os.path.dirname(IN_PATH), 'Converted')


def check_name(s):      # FIXME: regex?
    i = 0
    while i < len(s) - 3:
        if s[i] == 'S' and s[i + 3] == 'E':
            return int(s[(i + 1):(i + 3)]), int(s[(i + 4):(i + 6)])
        i += 1
    raise ValueError


def check_srt(file_name):
    lines = []
    with open(file_name, 'r') as file_data:
        for i, line in enumerate(file_data.readlines()):
            if 'http' in line or 'www' in line:
                lines.append(i + 1)
    return lines


def mkv_merge(in_file):
    name = os.path.basename(in_file)
    dir_name = os.path.dirname(in_file)

    try:
        s, e = check_name(name)
    except ValueError:
        print 'Cannot infer season & episode IDs for %s!' % in_file
        return

    out_path = os.path.join(OUT_PATH, 'Season %d' % s)
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    out_file = os.path.join(out_path, 'Episode %d.mkv' % e)

    try:
        srt = [f for f in os.listdir(dir_name) if f.endswith('.srt')]
        assert srt

        if len(srt) > 1:
            srt = [f for f in srt if 'eng' in f.lower()]

        srt = os.path.join(dir_name, srt[0])
        lines = check_srt(srt):
        if lines:
            raw_input('%s needs fix in lines %s!\nContinue?' % (srt, ', '.join(lines)))

    except AssertionError, IndexError:
        print 'SRT not found for %s!' % in_file
        return

    command = ' '.join(DEFAULT) % (out_file, in_file, srt)
    print 'Muxing ...\n'
    exec_cmd(command)


if __name__ == '__main__':
    args = sys.argv[1:]
    path = args.pop(0) if args else IN_PATH
    ext = args.pop(0) if args else 'mkv'

    if not os.path.exists(OUT_PATH):
        os.mkdir(OUT_PATH)

    for in_file in search(path, '.' + ext):
        if any(in_file.endswith(e) for e in ALLOWED):
            mkv_merge(in_file)
