execfile('Python Cleanup.py')
import eyed3, os, sys, shutil
from PIL import Image
from time import sleep

# A script to cleanup my soundtracks...
# It generates a json file, parses that as a dictionary and applies it to the tracks
# any changes we want, can be made to that json file using regex search & replace

path = '~/Desktop/TEMP'
colors = { 'R': '91', 'G': '92', 'Y': '93', 'B2': '94', 'P': '95', 'B1': '96', 'W': '97', '0': '0', }

def fmt(color = '0'):
    return {'win32': ''}.get(sys.platform, '\033[' + colors[color] + 'm')

avoid_titles = ['in', 'by', 'am', 'a', 'an', 'if', 'is', 'on', 'or',
                'the', 'for', 'not', 'of', 'to', 'at', 'be', 'vs']
# I prefer punctuations over some words and hyphen over some punctuations
word_subs = { 'and': '&' }
prefer_hyphen = ':_/'
careful_check = ')-:,]/'
avoid_start = ['the', 'an', 'a']            # filenames must not begin with articles!
allowed_puncs = '#!$&\'(),-.'               # symbols that can be allowed for track titles
avoid_puncs = '"%*+/:;<=>?@[\\]^_`{|}~'     # symbols to be avoided for filenames

def get_caps(string):
    return ''.join(s for s in string if s.isupper() or s.isdigit() or s in allowed_puncs)

def split_and_strip(string, puncs = '/;,'):     # filter common separators for artists
    split_strip = map(lambda s: s.strip(), string.split(puncs[0]))
    if puncs == puncs[-1]:
        return split_strip
    else:
        new_string = puncs[1].join(split_strip)
    return split_and_strip(new_string, puncs[1:])

def check_name(string, is_filename = False):    # custom names and titles for tracks
    split_list = string.split()
    corrected = []
    for i, word in enumerate(split_list):
        lower = word.lower()
        # title cases are always allowed for first & last words and if the previous word is a '-' or '&'
        if all([i > 0, i < len(split_list) - 1, split_list[i - 1] not in '-&/',
                ''.join(split_and_strip(lower, careful_check)) in avoid_titles]):
            corrected.append(lower)
        elif i > 0 and lower in word_subs:
            corrected.append(word_subs[lower])
        else:
            corrected.append(word[0].upper() + word[1:])
    if is_filename:
        corrected = [''.join(['-' if s in prefer_hyphen \
                                  else '' if s in avoid_puncs \
                                      else s for s in word])
                        for i, word in enumerate(corrected)
                            if (i > 0 or word.lower() not in avoid_start)]
    new_string = ''.join("'" if s == '"' else '(' if s == '[' else ')' if s == ']' \
                             else s for s in ' '.join(corrected))
    return new_string

def check_image(file_path, size = 400):
    if not os.path.exists(file_path):
        return False, "Image doesn't exist at the given location! (%s)" % file_path
    img = Image.open(file_path)
    width, height = img.size
    if width == height:
        if width < size:
            return False, 'Image size should be at least %s!' % size
        elif width > size:
            img.thumbnail((size, size), Image.ANTIALIAS)
            img.save(file_path)
        return True, None
    return False, 'Image width & height should be equal!'

def get_metadata(path):     # walk over a given path and get the metadata of MP3 files
    print
    temp_loc = os.path.join(path, 'TEMP')
    meta_data, image_data = [], {}
    mime = { 'image/jpeg': '.jpg', 'image/jpg': '.jpg', 'image/png': '.png' }
    files = search(path, '.mp3') + search(path, '.MP3')
    if not files:
        return False
    i, total = 1, len(files)
    for file_path in files:         # title, album, artist & year is what we need
        tag = eyed3.load(file_path).tag
        filename = os.path.basename(file_path).split('.')[0]
        album = check_name(tag.album) if tag.album else ''
        artist = '/'.join(map(check_name, split_and_strip(tag.artist))) if tag.artist else ''
        title = check_name(tag.title) if tag.title else check_name(filename)
        year = tag.best_release_date.year if tag.best_release_date else ''
        new_name = check_name('%s - %s - %s' % (title, get_caps(album), get_caps(artist)), True)

        lookup_key = album if album else title
        if year:    # all these workarounds are just to prevent name collisions in cover images
            lookup_key += ' (%d)' % year
        image_path = image_data.get(lookup_key)
        if not image_path:
            image_path = os.path.join(temp_loc, lookup_key)
            if tag.images:
                image_path += mime[tag.images[0].mime_type]
                with open(image_path, 'wb') as File:
                    File.write(tag.images[0].image_data)
                image_data[lookup_key] = image_path

        string = u'"{}": {{\n\t'    # write a viewable dictionary to file
        string += ',\n\t'.join((u'"name": "{}"', u'"cover": "{}"',
                                u'"title": "{}"', u'"album": "{}"',
                                u'"artist": "{}"', u'"year": "{}",',))
        string += u'\n}}'
        meta = string.format(file_path.decode('utf-8'), new_name,
                             image_data.get(lookup_key, 'NONE'),
                             title, album, artist, year)
        meta_data.append(meta)
        sys.stdout.write('\r Reading files... (%d/%d)' % (i, total))
        sys.stdout.flush()
        i += 1
    with open(os.path.join(temp_loc, 'TEMP.json'), 'w') as File:
        meta_data = ',\n'.join(meta_data)
        File.write(meta_data.encode('utf-8'))
    return True

def change_meta(rel_path = path, meta_exists = False):      # get the dumped metadata and modify the files
    path = os.path.expanduser(rel_path)
    eyed3.log.setLevel("ERROR")
    temp_loc = os.path.join(path, 'TEMP')
    if not os.path.exists(temp_loc):
        os.mkdir(temp_loc)
    json = os.path.join(temp_loc, 'TEMP.json')
    if (meta_exists and not os.path.exists(json)) or (not meta_exists and not get_metadata(path)):
        print '%s Nothing to work!%s' % (fmt('R'), fmt())
        return
    if not meta_exists:
        raw_input('\nMetadata has been dumped! Continue after making changes...')
    while True:
        with open(json) as File:
            data = File.read().decode('utf-8')
        try:
            print
            errors = []
            exec('meta_data = {' + data + '}')     # Look at this awesomesauce!
            stuff = meta_data.items()
            i, total = 1, len(stuff)
            for file_path, data in stuff:
                decoded_path = file_path.decode('utf-8')
                try:        # yeah, I'm being strict here - all these attributes are necessary for me
                    year = data['year']
                    data_req = { 'Album name': data['album'],
                                 'Album cover': data['cover'],
                                 'Artist name': data['artist'],
                                 'Year': year }
                except KeyError as err:
                    errors.append((decoded_path, "Missing '%s'!" % err.args[0]))
                for attr, val in data_req.items():
                    if not val:     # cover is optional, so let's just pretend that we have it
                        errors.append((decoded_path, '%s not found!' % attr))
                if year:
                    try:
                        data['year'] = int(year)        # check if a valid year is given
                    except ValueError:
                        errors.append((decoded_path, 'Year should be in the form of numbers!'))
                image_path = data['cover']
                if image_path != 'NONE':                # check the cover image
                    success, fail_reason = check_image(image_path)
                    if not success:
                        errors.append((decoded_path, fail_reason))
                sys.stdout.write('\r Checking files... (%d/%d)' % (i, total))
                sys.stdout.flush()
                i += 1
            if not errors:
                break
            print
            for filename, reason in errors:
                print '{}{}: {}{}{}'.format(fmt('Y'), filename, fmt('R'), reason, fmt())
            raw_input('\nErrors found! Continue after fixing them...')
        except Exception as err:
            print err
            print '%sCannot parse some of the values. Make sure that all the data are in strings!%s' \
                   % (fmt('R'), fmt())
            raw_input('Continue after fixing it...')

    i = 1
    mime = { '.jpg': 'image/jpeg', '.png': 'image/png' }
    print
    for file_path, data in stuff:
        tag = eyed3.load(file_path).tag
        tag.clear()
        tag.album, tag.artist, tag.title = map(lambda s: s.decode('utf-8'),
                                               (data['album'], data['artist'], data['title']))
        tag.release_date, tag.recording_date, tag.original_release_date = [data['year']] * 3
        image_path = data['cover']
        if image_path != 'NONE':
            ext = image_path[image_path.rfind('.'):]
            with open(image_path, 'rb') as image:
                tag.images.set(3, image.read(), mime[ext], tag.album)
        tag.save(file_path)
        file_dir = os.path.dirname(file_path)
        filename = os.path.join(file_dir, data['name'])
        meta_data[file_path] = filename
        sys.stdout.write('\r Applying attributes... (%d/%d)' % (i, total))
        sys.stdout.flush()
        i += 1
    i = 1
    print
    for old_name, new_name in meta_data.items():
        os.rename(old_name, new_name + '.mp3')
        sys.stdout.write('\r Renaming files... (%d/%d)' % (i, total))
        sys.stdout.flush()
        i += 1
    shutil.rmtree(temp_loc)
    print '\n\n{}Yay! Cleaned up everything!{}'.format(fmt('G'), fmt())
