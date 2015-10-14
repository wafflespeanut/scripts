execfile('Python Cleanup.py')
import os, eyed3

# I'm a perfectionist!

path = os.path.expanduser('~/Desktop/TEMP')
files_list = search(path, '.mp3')

def check_name(string, is_filename = False):
    avoid_upper = ['the', 'for', 'a', 'an', 'if', 'of', 'to', 'is']
    avoid_puncs = '"#$%*+./:;<=>?@[\\]^_`{|}~'     # possible symbols to be avoided for MP3 filenames
    corrected = [word.lower() if (word.lower() in avoid_upper and i > 0) \
                              else word.upper() for i, word in enumerate(string.split())]
    if is_filename:
        corrected = [''.join([s for s in word if s not in avoid_puncs])\
                     for word in string.split()]
    return ' '.join(corrected)

def get_metadata(files = files_list):
    for file_path in files:
        meta_data = {}
        tag = eyed3.load(file_path).tag
        artist, album, title, year = tag.artist, tag.album, tag.title, tag.best_release_date.year
        filename, ext = os.path.basepath(file_path).split('.')
        dirname = os.path.dirname(file_path)
        album = ' '.join(map(lambda string: string.upper(), album.split()))
        artist = ' '.join(map(lambda string: string.upper(), artist.split()))
        title = check_name(title)
        new_name = check_name(filename, True)
        meta_data[filename] = dict([('name', new_name) \
                                    ('artist', artist), ('album', album), \
                                    ('title', title), ('year', year)])
