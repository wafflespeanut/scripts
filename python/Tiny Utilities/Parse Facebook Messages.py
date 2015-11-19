# Parse the "messages.htm" file in your Facebook data
# Nothing useful, I just wanna see my history

import os

TAB_WIDTH = 4
file_path = os.path.expanduser('~/Desktop/')
file_name = 'messages.htm'

def cleanup_html(path = file_path):         # Firstly, cleanup the HTML for readability
    i, spaces, clean_data = 0, 0, ''
    expect_tag = []
    with open(path + file_name, 'r') as file_data:
        data = ''.join(file_data.readlines())
    max_length = len(data)
    while i < max_length:
        if data[i] == '<' and data[i + 1] != '/':
            expect_tag.append(True)
            clean_data += spaces * ' '
            spaces += TAB_WIDTH
            while data[i] != '>':
                clean_data += data[i]
                i += 1
            if data[i - 1] == '/':
                expect_tag.pop()
                spaces -= TAB_WIDTH
            clean_data += '>\n'
        elif expect_tag and expect_tag[-1] and data[i] == '<' and data[i + 1] == '/':
            if expect_tag.pop():
                spaces -= TAB_WIDTH
            clean_data += ' ' * spaces
            while data[i] != '>':
                clean_data += data[i]
                i += 1
            clean_data += '>\n'
        if expect_tag and expect_tag[-1]:
            i += 1
            if i < max_length and data[i] != '<':
                clean_data += ' ' * spaces
                while i < max_length and data[i] != '<':
                    clean_data += data[i]
                    if data[i] == '\n':
                        clean_data += ' ' * spaces
                    i += 1
                clean_data += '\n'
            i -= 1
        i += 1
    with open(path + 'cleaned_' + file_name, 'w') as file_buff:
        file_buff.write(clean_data)
