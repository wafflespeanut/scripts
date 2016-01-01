try:
    import eyed3, os, sys, shutil
    from PIL import Image
    from time import sleep
except ImportError:
    print "You'll be needing 'PIL' & 'eyed3' modules for this thing!"

# A script to cleanup my soundtracks...
# It generates a json file, parses that as a dictionary and applies it to the tracks
# any changes we want, can be made to that json file using regex search & replace

def search(path, ext = '.py'):                           # For listing all those .py files
    file_list = []
    for root, dirs, files in os.walk(path):
        file_list.extend([os.path.join(root, f) for f in files if f.endswith(ext) or f.endswith(ext.upper())])
    return sorted(file_list)

path = '~/Desktop/TEMP'
colors = { 'R': '91', 'G': '92', 'Y': '93', 'B2': '94', 'P': '95', 'B1': '96', 'W': '97', '0': '0', }

def fmt(color = '0'):
    return {'win32': ''}.get(sys.platform, '\033[' + colors[color] + 'm')

avoid_titles = ['in', 'by', 'am', 'a', 'an', 'if', 'is', 'on', 'or', 'not',
                'the', 'for',  'of', 'to', 'at', 'be', 'from', 'vs']
# I prefer punctuations over some words and hyphen over some punctuations
word_subs = { 'and': '&' }
prefer_hyphen = ':_/'
careful_check = ')-:,]/'
avoid_start = ['the', 'an', 'a']            # filenames must not begin with articles!
allowed_puncs = '#!$&\'(),-.'               # symbols that can be allowed for track titles
avoid_puncs = '"%*+/:;<=>?@[\\]^_`{|}~'     # symbols to be avoided for filenames

def get_caps(string):
    return ''.join(s for s in string if s.isupper() or s.isdigit() or s in allowed_puncs)

def split_and_strip(string, puncs = '/;,'):     # filter common separators for words
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
    files = search(path, '.mp3')
    if not files:
        return False
    i, total = 1, len(files)

    def attr_from_comments(tag, attr_val, idx, check_func, alternative = lambda _val: ''):
        if tag.comments:    # We can be quite sure here, because we're gonna erase everything else
            attrs = tag.comments[0].text.split('|||')   # our separator for those attributes
            if len(attrs) > idx:
                if attr_val and attrs[idx] and attr_val == attrs[idx]:
                    return attr_val, 'true'
        return check_func(attr_val) if attr_val else alternative(attr_val), 'false'

    for file_path in files:         # title, album, artist & year is what we need
        tag = eyed3.load(file_path).tag
        filename = os.path.basename(file_path).split('.')[0]
        album = check_name(tag.album) if tag.album else ''
        artist = '/'.join(map(check_name, split_and_strip(tag.artist))) if tag.artist else ''
        # If we wanna force the title, album or artist (i.e., don't want the machine output)
        # we can store them in the comments and check against the existing tag attributes
        title, forced_title = attr_from_comments(tag, tag.title, 0, check_name, lambda _val: check_name(filename))
        album, forced_album = attr_from_comments(tag, tag.album, 1, check_name)
        artist, forced_artist = attr_from_comments(tag, tag.artist, 2,
                                                  lambda val: '/'.join(map(check_name, split_and_strip(val))))
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
                                u'"title": "{}"', u'"forced_title": {}',
                                u'"album": "{}"', u'"forced_album": {}',
                                u'"artist": "{}"', u'"forced_artist": {}',
                                u'"year": {}'))
        string += u'\n}}'
        meta = string.format(file_path.decode('utf-8'), new_name,
                             image_data.get(lookup_key, 'NONE'),
                             title, forced_title, album, forced_album,
                             artist, forced_artist, year)
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
            true, false = True, False
            attrs = ['title', 'album', 'artist']
            errors = []
            exec 'meta_data = {' + data + '}' in globals(), locals()    # awesomesauce!
            stuff = meta_data.items()
            i, total = 1, len(stuff)
            for file_path, data in stuff:
                decoded_path = file_path.decode('utf-8')
                try:        # yeah, I'm being strict here - all these attributes are necessary for me
                    assert int(data['year']) > 1900, "songs didn't exist back then!"
                    for attr in attrs:
                        assert type(data['forced_' + attr]) is bool, 'forced_%s should be a bool!' % attr
                        assert data[attr], '%s not found!' % attr
                except KeyError as err:
                    errors.append((decoded_path, "missing '%s'!" % err.args[0]))
                except ValueError:
                    errors.append((decoded_path, 'year should be in the form of numbers!'))
                except AssertionError as err:
                    errors.append((decoded_path, err))
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
            print '%sCannot parse some of the values. Make sure that the data is in JSON format!%s' \
                   % (fmt('R'), fmt())
            raw_input('Continue after fixing it...')

    i = 1
    mime = { '.jpg': 'image/jpeg', '.png': 'image/png' }
    print
    for file_path, data in stuff:
        tag = eyed3.load(file_path).tag
        tag.clear()
        attr_objs = tag.title, tag.album, tag.artist = map(lambda s: data[s].decode('utf-8'), attrs)
        tag.release_date, tag.recording_date, tag.original_release_date = map(str, [data['year']] * 3)
        image_path = data['cover']
        if image_path != 'NONE':
            ext = image_path[image_path.rfind('.'):]
            with open(image_path, 'rb') as image:
                tag.images.set(3, image.read(), mime[ext], tag.album)
        # Too bad that I have to index stuff here...
        comment = u'|||'.join(map(lambda idx: attr_objs[idx] if data['forced_' + attrs[idx]] else 'NONE',
                                  range(len(attrs))))      # This doesn't work due to exec's limitation
        tag.comments.set(comment)
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
