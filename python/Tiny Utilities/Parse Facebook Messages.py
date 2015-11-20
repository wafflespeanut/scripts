# Parse the "messages.htm" file in your Facebook data
# Nothing useful or interesting, other than a cumbersome counting
# I just wanted to review my history

# FIXME: Rewrite the thing to build a dictionary (JSON or tree structure, whatever you wanna call it)
# out of the HTML, so that we can traverse through the keys whenever we want (which is way more elegant)

import os
from datetime import datetime

TAB_WIDTH = 4
file_path = os.path.expanduser('~/Desktop/')
file_name = 'messages.htm'
new_name = 'clean_messages.htm'

def cleanup_html(path = file_path + file_name):
    '''
    Prettify an uglified (a.k.a., minified) HTML. Note that this works only for the minified version!
    Since this doesn't check for whitespaces, partially (or) fully cleaned up files may be screwed up!
    '''
    i, spaces, clean_data = 0, 0, ''
    expect_tag = []
    with open(path, 'r') as file_data:
        data = ''.join(file_data.readlines())
    max_length = len(data)
    while i < max_length:               # FIXME: HTML -> JSON & indexing -> iterator
        if data[i] == '<' and data[i + 1] != '/':
            expect_tag.append(True)         # which means we're inside a block
            clean_data += ' ' * spaces
            spaces += TAB_WIDTH
            while data[i] != '>':
                clean_data += data[i]
                i += 1
            if data[i - 1] == '/':      # tags like <br/>, <link ... />, or <meta ... />
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
        if expect_tag and expect_tag[-1]:       # grab everthing inside a block (especially for <p> ... </p>)
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
    with open(file_path + new_name, 'w') as file_buff:
        file_buff.write(clean_data)

def parse_to_dict():    # a terrible excuse for a parser, really!
    with open(file_path + new_name, 'r') as file_data:
        data = map(lambda line: line.strip(), file_data.read().split('\n'))
    i, length, parsed = 0, len(data), {}
    while i < length:   # find the user (we don't need any stuff other than the messages)
        if data[i] == '<div class="contents">':     # FIXME: prefer regex for finding tags instead of raw-comparison
            i += 2
            username = data[i][:]
            break
        i += 1
    while i < length:                   # FIXME: HTML -> JSON & indexing -> iterator
        is_in_thread = False
        if data[i] == '<div class="thread">':
            is_in_thread = True
            i += 1
            people = data[i][:]
            # we can safely reset this because the conversations are in (descending) order, and we won't lose anything!
            parsed[people] = []
        while is_in_thread and i < length:
            if data[i] == '<div class="thread">':
                is_in_thread = False
            elif data[i] == '<span class="user">':
                parsed[people] += [data[i + 1]]     # get the participant's name
                i += 4      # parse the timestamp into a datetime object
                parsed[people] += [datetime.strptime(data[i], '%A, %d %B %Y at %H:%M UTC+05:30')]
                i += 5      # wheee... skipping happily because the structure is so predictable!
                parsed[people].append('')
                while data[i] != '</p>':    # grab the contents and chain replacements (probably inefficient)
                    parsed[people][-1] += data[i].replace('&#039;', "'").replace('&amp;', '&').replace('&quot;', '"')
                    i += 1
            i += 1
        i += 1
    return parsed

if __name__ == '__main__':
    cleanup_html()      # once we clean this up, it's pretty easy to parse it (efficiency doesn't matter here)
    parsed_dict = parse_to_dict()
