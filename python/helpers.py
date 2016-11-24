import os, sys, subprocess


def exec_cmd(command, call=lambda s: sys.stdout.write(s) and sys.stdout.flush(),
             print_cmd=True, prefer_lines=True, needs_output=True):
    output = []
    if print_cmd:
        print '\033[93m%s\033[0m' % command
    process = subprocess.Popen(command, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE, shell=True)
    if call:
        line = ''
        for char in iter(lambda: process.stdout.read(1), ''):
            line += char
            if char == '\n':
                output.append(line)
                line = ''
                if prefer_lines:
                    call(output[-1])
                    continue
            if not prefer_lines:
                call(char)

    process.wait()
    if needs_output:
        return ''.join(output)


def search(path, ext):
    file_list = []
    for root, dirs, files in os.walk(path):
        file_list.extend([os.path.join(root, f) for f in files if f.lower().endswith(ext)])
    return sorted(file_list)
