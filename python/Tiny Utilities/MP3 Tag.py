execfile('Python Cleanup.py')
import eyed3, os, sys
from PIL import Image

# A script to cleanup my soundtracks...
path = os.path.expanduser('~/Desktop/TEMP')

colors = { 'R': '91', 'G': '92', 'Y': '93', 'B2': '94', 'P': '95', 'B1': '96', 'W': '97', '0': '0', }

def fmt(color = '0'):
    return {'win32': ''}.get(sys.platform, '\033[' + colors[color] + 'm')

def split_and_strip(string, puncs = '/;,'):     # filter common separators for artists
    split_strip = map(lambda s: s.strip(), string.split(puncs[0]))
    if len(puncs) == 1:
        return split_strip
    else:
        new_string = puncs[1].join(split_strip)
    return split_and_strip(new_string, puncs[1:])

def check_name(string, is_filename = False):    # custom names and titles for tracks
    avoid_titles = ['the', 'for', 'a', 'an', 'if', 'is', 'on',   # I hate when these have title cases
                    'in', 'by', 'am', 'not', 'of', 'to', 'at']
    subs = {'and': '&'}     # I also prefer to substitute
    avoid_start = ['the', 'an', 'a']            # I prefer filenames to not begin with articles
    allowed_puncs = '!&\'(),-'                  # symbols that can be allowed for track titles
    avoid_puncs = '"#$%*+./:;<=>?@[\\]^_`{|}~'  # possible symbols to be avoided for MP3 filenames

    split_list = string.split()
    lim = len(split_list) - 1
    corrected = []
    for i, word in enumerate(split_list):
        lower = word.lower()
        if all([i > 0, i < lim, lower in avoid_titles, split_list[i - 1] not in '-&']):
            # title cases are always allowed for first & last words and if the previous word is a '-' or '&'
            corrected.append(lower)
        elif i > 0 and lower in subs:
            corrected.append(subs[lower])
        else:
            corrected.append(word[0].upper() + word[1:])

    if is_filename:
        corrected = [''.join([s for s in word if s not in avoid_puncs])
                        for i, word in enumerate(corrected)
                            if (i > 0 or word.lower() not in avoid_start)]
    new_string = ' '.join(corrected)
    return new_string

def get_metadata(path):           # walk over a given path and get the metadata of MP3 files
    print
    meta_data = []
    files = search(path, '.mp3')
    i, total = 1, len(files)
    for file_path in files:         # title, album, artist & year is what we need
        tag = eyed3.load(file_path).tag
        filename = os.path.basename(file_path).split('.')[0]
        album = check_name(tag.album) if tag.album else ''
        artist = '/'.join(map(check_name, split_and_strip(tag.artist))) if tag.artist else ''
        title = check_name(tag.title) if tag.title else check_name(filename)
        year = tag.best_release_date.year if tag.best_release_date else ''
        new_name = check_name(title, True)
        string = u'"{}": {{\n\t'    # write a viewable dictionary to file
        string += u', '.join((u'"name": "{}"',
                              u'\n\t"title": "{}"', u'"album": "{}"',
                              u'\n\t"artist": "{}"', u'"year": "{}"',))
        string += u'\n}}'
        meta = string.format(file_path.decode('utf-8'), new_name, title, album, artist, year)
        meta_data.append(meta)
        sys.stdout.write('\rReading files... (%d/%d)' % (i, total))
        i += 1
    with open('TEMP.json', 'w') as File:
        meta_data = u'{\n\n' + u',\n'.join(meta_data) + u'\n\n}'
        File.write(meta_data.encode('utf-8'))

def change_meta(path = path):       # get the dumped metadata and modify the files
    get_metadata(path)
    raw_input('\nMetadata has been dumped! Continue after making changes...')
    while True:
        with open('TEMP.json') as File:
            data = File.read().decode('utf-8')
        try:
            print
            errors = []
            exec('meta_data = ' + data)     # awesomesauce!
            stuff = meta_data.items()
            i, total = 1, len(stuff)
            for file_path, data in stuff:
                decoded_path = file_path.decode('utf-8')
                try:
                    year = data['year']
                    all_data = { 'Album name': data['album'], 'Artist name': data['artist'], 'Year': year }
                except KeyError as err:
                    errors.append((decoded_path, "Missing '%s'!" % err.args[0]))
                for attr, val in all_data.items():
                    if not val:     # yeah, I'm being strict here - all these attributes are necessary
                        errors.append((decoded_path, '%s not found!' % attr))
                if year:
                    try:
                        data['year'] = int(year)
                    except ValueError:
                        errors.append((decoded_path, 'Year should be in the form of numbers!'))
                sys.stdout.write('\rChecking files... (%d/%d)' % (i, total))
                i += 1
            if not errors:
                break
            print
            for filename, reason in errors:
                print '{}{}: {}{}{}'.format(fmt('Y'), filename, fmt('R'), reason, fmt())
            raw_input('\nErrors found! Continue after fixing them...')
        except Exception:
            print '%sCannot parse some of the values. Make sure that all the data are in strings!%s' \
                   % (fmt('R'), fmt())
            raw_input('Continue after fixing it...')

    i = 1
    print
    for file_path, data in stuff:
        tag = eyed3.load(file_path).tag
        tag.clear()
        tag.album, tag.artist, tag.title = map(lambda s: s.decode('utf-8'),
                                               (data['album'], data['artist'], data['title']))
        tag.release_date, tag.recording_date, tag.original_release_date = [data['year']] * 3
        tag.save(file_path)
        file_dir = os.path.dirname(file_path)
        os.rename(file_path, os.path.join(file_dir, data['name'] + '.mp3'))
        sys.stdout.write('\rApplying attributes... (%d/%d)' % (i, total))
        i += 1
    os.remove('TEMP.json')
    print '\n\n{}Yay! Cleaned up everything!{}'.format(fmt('G'), fmt())
