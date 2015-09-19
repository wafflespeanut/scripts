# a rough script to reduce the work for https://github.com/servo/servo/pull/7546
import os

def get_file_data(name):
    with open(name, 'r') as File:
        return File.readlines()

i = 0
data = get_file_data(os.path.expanduser('~/Desktop/TEMP'))
while i < len(data):
    if 'warning' in data[i] and 'alphabetical order' in data[i]:
        span = data[i].split(':')
        (file_name, span_start, span_end) = (span[0], int(span[1]) - 1, int(span[3]) - 1)
        i += 3
        suggested = []
        while data[i] != '\n':
            suggested.append(data[i])
            i += 1
        suggestion = '\n======\n{} SUGGESTED <<<<<<\n'.format(''.join(suggested))
        file_data = get_file_data(file_name)
        file_data[span_start] = "\n>>>>>> EXISTING\n" + file_data[span_start]
        file_data[span_end] += suggestion
        with open(file_name, 'w') as File:
            File.writelines(file_data)
        raw_input("\nWrote on file: %s\nContinue after making changes..." % file_name)
    i += 1
