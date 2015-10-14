execfile('Python Cleanup.py')
import os, eyed3

# I'm a perfectionist!

path = os.path.expanduser('~/Desktop/TEMP')

def check_name(string, is_filename = False):
    avoid_upper = ['the', 'for', 'a', 'an', 'if', 'is', 'on',
                   'in', 'by', 'am', 'not', 'of', 'to', 'at']
    subs = {'and': '&'}
    avoid_start = ['the', 'an', 'a']
    avoid_puncs = '"#$%*+./:;<=>?@[\\]^_`{|}~'     # possible symbols to be avoided for MP3 filenames
    split_list = string.split()
    lim = len(split_list) - 1
    corrected = [word.lower() if (word.lower() in avoid_upper and i > 0 and i < lim)
                    else subs[word.lower()] if (word.lower() in subs and i > 0)
                        else word.title() for i, word in enumerate(split_list)]
    if is_filename:
        corrected = [''.join([s for s in word if s not in avoid_puncs])
                        for i, word in enumerate(corrected)
                            if (i > 0 or word.lower() not in avoid_start)]
    new_string = ' '.join(corrected)
    if "'" in new_string:
        sliced = new_string.split("'")
        new_string = sliced[0] + "'" + sliced[1][0].lower() + sliced[1][1:]
    return new_string

# def get_metadata(path = path):
meta_data = []
files = search(path, '.mp3')
for file_path in files:
    tag = eyed3.load(file_path).tag
    year = tag.best_release_date.year
    filename = os.path.basename(file_path).split('.')[0]
    album = ' '.join(map(lambda string: string.title(), tag.album.split()))
    artist = ' '.join(map(lambda string: string.title(), tag.artist.split()))
    title = check_name(tag.title)
    new_name = check_name(filename, True)
    string = "\"{}\": {{\n\t"
    string += ', '.join(("'name': \"{}\"",
                         "\n\t'title': \"{}\"", "'album': \"{}\"",
                         "\n\t'artist': \"{}\"", "'year': {},"))
    string += '\n}}'
    meta_data.append(string.format(file_path, new_name, title, album, artist, year))
with open('TEMP.json', 'w') as File:
    File.write('{\n' + ',\n'.join(meta_data) + '\n}')
