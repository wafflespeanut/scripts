import os, sys, subprocess

def print_line(line):
    sys.stdout.write(line)
    sys.stdout.flush()

def exec_cmd(command, call = print_line):
    output = []
    print command
    process = subprocess.Popen(command, stderr = subprocess.STDOUT,
                               stdout = subprocess.PIPE, shell = True)
    if call:
        stdout_lines = iter(process.stdout.readline, "")
        for line in stdout_lines:   # do something as and whenever we get an output
            output.append(line)
            call(line)

    _out, error = process.communicate()
    if error:
        print 'ERROR: %s' % error
    return ''.join(output)


def search(path, ext):
    file_list = []
    for root, dirs, files in os.walk(path):
        file_list.extend([os.path.join(root, f) for f in files if f.lower().endswith(ext)])
    return sorted(file_list)
