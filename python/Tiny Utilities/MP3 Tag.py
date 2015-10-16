execfile('Python Cleanup.py')
import eyed3, os, sys

# A script to cleanup my soundtracks...
path = os.path.expanduser('~/Desktop/TEMP')

def check_name(string, is_filename = False):    # custom names and titles for tracks
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

def get_metadata(path):           # walk over a given path and get the metadata of MP3 files
    print
    meta_data = []
    files = search(path, '.mp3')
    i, total = 1, len(files)
    for file_path in files:         # title, album, artist & year is what we need
        tag = eyed3.load(file_path).tag
        filename = os.path.basename(file_path).split('.')[0]
        year = tag.best_release_date.year if tag.best_release_date else None
        album = ' '.join(map(lambda string: string.title(), tag.album.split())) if tag.album else None
        artist = ' '.join(map(lambda string: string.title(), tag.artist.split())) if tag.artist else None
        title = check_name(tag.title) if tag.title else check_name(filename)
        new_name = check_name(title, True)
        string = "%r: {\n\t"       # write a viewable dictionary to file
        string += ', '.join(("'name': %r",
                             "\n\t'title': %r", "'album': %r",
                             "\n\t'artist': %r", "'year': %r,"))
        string += '\n}'
        meta_data.append(string % (file_path, new_name, title, album, artist, year))
        sys.stdout.write('\rReading files... (%d/%d)' % (i, total))
        i += 1
    with open('TEMP.json', 'w') as File:
        File.write('{\n\n' + ',\n'.join(meta_data) + '\n\n}')

def change_meta(path = path):
    get_metadata(path)
    raw_input('\nMetadata has been dumped! Continue after making changes... ')
    with open('TEMP.json') as File:
        data = File.read()
    while True:
        try:
            errors = []
            exec('meta_data = ' + data)     # awesomesauce of interpreters!
            stuff = meta_data.items()
            i, total = 1, len(stuff)
            for file_path, data in stuff:
                year = data['year']
                all_data = { 'Album name': data['album'], 'Artist name': data['artist'], 'Year': year }
                for attr, val in all_data.items():
                    if not val:
                        err = '%s not found for %s' % (attr, file_path)
                        errors.append(err)
                if year and type(year) is not int:
                    try:
                        data['year'] = int(year)
                    except ValueError:
                        errors.append('Year should be in the form of numbers for %s' % file_path)
            if not errors:
                break
            print '\n' + '\n'.join(errors)
            raw_input('\nErrors found! Continue after fixing them...')
            with open('TEMP.json') as File:
                data = File.read()
        except Exception:
            print '\nCannot parse some of the values. Make sure that all the data are in strings!'
            raw_input('Continue after fixing it...')

    for file_path, data in stuff:
        tag = eyed3.load(file_path).tag
        tag.clear()
        tag.album, tag.artist, tag.title = unicode(data['album']), unicode(data['artist']), unicode(data['title'])
        tag.release_date, tag.recording_date, tag.original_release_date = [data['year']] * 3
        tag.save(file_path)
        file_dir = os.path.dirname(file_path)
        os.rename(file_path, os.path.join(file_dir, data['name'] + '.mp3'))
    os.remove('TEMP.json')
    print 'Yay! Cleaned up everything!'
