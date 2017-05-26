try:
    import eyed3, os, sys, shutil
    from PIL import Image
except ImportError:
    print "You'll be needing 'PIL' & 'eyed3' modules for this thing!"

from time import sleep
import os, inspect, json, sys

filename = inspect.getframeinfo(inspect.currentframe()).filename
exec_path = os.path.dirname(os.path.abspath(filename))
execfile(os.path.join(exec_path, 'helpers.py'))

# A script to cleanup my soundtracks... (it's quite old, and I'm too lazy to refactor it)
# It generates a json file, on which we can make our changes using regex search & replace
# FIXME: Refactor (one day) and prefer a Mp3Tagger class

SEP = u'|||'
PATH = '~/Desktop/TEMP'
COLORS = { 'R': '91', 'G': '92', 'Y': '93', 'B2': '94', 'P': '95', 'B1': '96', 'W': '97', '0': '0', }

def fmt(color = '0'):
    return {'win32': ''}.get(sys.platform, '\033[' + COLORS[color] + 'm')


avoid_titles = ['in', 'by', 'am', 'a', 'an', 'if', 'is', 'on', 'or', 'not',
                'the', 'for', 'of', 'to', 'at', 'be', 'from', 'vs']
# I prefer punctuations over some words and hyphen over some punctuations
word_subs = { 'and': '&' }
prefer_hyphen = ':_/'
careful_check = ')-:,]/'
avoid_start = ['the', 'an', 'a']            # filenames must not begin with articles!
allowed_puncs = '#!$&\'(),-.'               # symbols that can be allowed for track titles
avoid_puncs = '!"%*+/:;<=>?@[\\]^_`{|}~'    # symbols to be avoided for filenames

def get_titled(string):
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
        return "Image doesn't exist at the given location! (%s)" % file_path
    img = Image.open(file_path)
    width, height = img.size

    if width == height:
        if width < size:
            return 'Image size should be at least %s!' % size
        elif width > size:
            img.thumbnail((size, size), Image.ANTIALIAS)
            img.save(file_path)
        return
    return 'Image width & height should be equal!'


def get_metadata(path):     # walk over a given path and get the metadata of MP3 files
    print
    temp_loc = os.path.join(path, 'TEMP')
    metadata, image_data = {}, {}
    mime = { 'image/jpeg': '.jpg', 'image/jpg': '.jpg', 'image/png': '.png' }

    files = search(path, '.mp3')
    if not files:
        return 0
    i, total = 1, len(files)

    def attr_from_comments(tag, attr_val, idx, check_func, alternative = lambda _val: ''):
        if tag.comments:    # We can be quite sure here, because we're gonna erase everything else
            attrs = tag.comments[0].text.split(SEP)   # our separator for those attributes
            if len(attrs) > idx:
                if attr_val and attrs[idx] and attr_val == attrs[idx]:
                    return attr_val, True
        return check_func(attr_val) if attr_val else alternative(attr_val), False

    for file_path in files:         # title, album, artist & year is what we need
        tag = eyed3.load(file_path).tag
        filename = os.path.basename(file_path).split('.')[0]
        album = check_name(tag.album) if tag.album else ''
        artist = '/'.join(map(check_name, split_and_strip(tag.artist))) if tag.artist else ''

        # If we wanna force the title, album or artist (i.e., don't want the script output)
        # we can store them in the comments and check against the existing tag attributes
        title, forced_title = attr_from_comments(tag, tag.title, 0, check_name, lambda _val: check_name(filename))
        album, forced_album = attr_from_comments(tag, tag.album, 1, check_name)
        artist, forced_artist = attr_from_comments(tag, tag.artist, 2,
                                                  lambda val: '/'.join(map(check_name, split_and_strip(val))))
        year = tag.best_release_date.year if tag.best_release_date else None
        new_name = check_name('%s-%s-%s' % (title, get_titled(album), get_titled(artist)), True)
        new_name = '-'.join(new_name.split())

        lookup_key = album if album else title
        lookup_key += ' (%s)' % year    # workaround to prevent name collisions in cover images
        image_path = image_data.get(lookup_key)

        if not image_path:
            image_path = os.path.join(temp_loc, lookup_key)
            if tag.images:
                image_path += mime[tag.images[0].mime_type]
                with open(image_path, 'wb') as fd:
                    fd.write(tag.images[0].image_data)
                image_data[lookup_key] = image_path

        path = file_path.decode('utf-8')
        meta = {
            "name": new_name,
            "cover": image_data.get(lookup_key),
            "title": title,
            "forced_title": forced_title,
            "album": album,
            "forced_album": forced_album,
            "artist": artist,
            "forced_artist": forced_artist,
            "year": year,
        }

        metadata[path] = meta
        sys.stdout.write('\r Reading files... (%d/%d)' % (i, total))
        sys.stdout.flush()
        i += 1

    with open(os.path.join(temp_loc, 'TEMP.json'), 'w') as fd:
        json.dump(metadata, fd, indent = 2)
    return True


def change_meta(rel_path, meta_exists = False):     # get the dumped metadata and modify the files
    path = os.path.expanduser(rel_path)
    eyed3.log.setLevel("ERROR")
    temp_loc = os.path.join(path, 'TEMP')
    mime = { '.jpg': 'image/jpeg', '.png': 'image/png' }

    if not os.path.exists(temp_loc):
        os.mkdir(temp_loc)
    meta_file = os.path.join(temp_loc, 'TEMP.json')

    if (meta_exists and not os.path.exists(meta_file)) or (not meta_exists and not get_metadata(path)):
        print ' %sJSON file not found!%s' % (fmt('R'), fmt())
        return
    if not meta_exists:
        raw_input('\nMetadata has been dumped! Continue after making changes...')

    while True:
        print
        try:
            errors = []
            attrs = ['title', 'album', 'artist']

            with open(meta_file) as fd:
                metadata = json.load(fd)
            stuff = metadata.items()
            i, total = 1, len(stuff)

            for file_path, data in stuff:
                decoded_path = file_path.encode('utf-8')
                try:
                    assert int(data['year']) > 1900, "songs didn't exist before 1900!"
                    for attr in attrs:
                        assert type(data['forced_' + attr]) is bool, 'forced_%s should be a bool!' % attr
                        assert data[attr], '%s not found!' % attr
                except KeyError as err:
                    errors.append((decoded_path, "missing '%s'!" % err.args[0]))
                except ValueError:
                    errors.append((decoded_path, 'year should be a number!'))
                except AssertionError as err:
                    errors.append((decoded_path, err))

                image_path = data['cover']
                if image_path:      # check the cover image
                    fail_reason = check_image(image_path)
                    if fail_reason:
                        errors.append((decoded_path, fail_reason))

                sys.stdout.write('\r Checking files... (%d/%d)' % (i, total))
                sys.stdout.flush()
                i += 1

            print
            if not errors:
                break

            for filename, reason in errors:
                print '{}{}: {}{}{}'.format(fmt('Y'), filename, fmt('R'), reason, fmt())
            raw_input('\nErrors found! Continue after fixing them...')

        except Exception as err:
            print err
            print '%sCannot parse some of the values. Make sure that the data is in valid JSON format!%s' \
                   % (fmt('R'), fmt())
            raw_input('\nContinue after fixing it...')

    i = 1
    print

    for file_path, data in stuff:
        tag = eyed3.load(file_path).tag
        tag.clear()
        attr_objs = tag.title, tag.album, tag.artist = map(lambda s: data[s], attrs)
        tag.release_date, tag.recording_date, tag.original_release_date = map(str, [data['year']] * 3)
        image_path = data['cover']

        if image_path:
            ext = image_path[image_path.rfind('.'):]
            with open(image_path, 'rb') as image:
                tag.images.set(3, image.read(), mime[ext], tag.album)

        # Too bad that I have to index stuff here...
        comment = SEP.join(map(lambda idx: attr_objs[idx] if data['forced_' + attrs[idx]] else u'NONE',
                               range(len(attrs))))
        tag.comments.set(comment)
        tag.save(file_path)
        file_dir = os.path.dirname(file_path)
        filename = os.path.join(file_dir, data['name'])
        metadata[file_path] = filename
        sys.stdout.write('\r Applying attributes... (%d/%d)' % (i, total))
        sys.stdout.flush()
        i += 1
    i = 1

    print
    for old_name, new_name in metadata.items():
        os.rename(old_name, new_name + '.mp3')
        sys.stdout.write('\r Renaming files... (%d/%d)' % (i, total))
        sys.stdout.flush()
        i += 1

    shutil.rmtree(temp_loc)
    print '\n\n{}Yay! Cleaned up everything!{}'.format(fmt('G'), fmt())

if __name__ == '__main__':
    args = sys.argv[1:]
    path = args[0] if args else PATH
    change_meta(path.rstrip('!'), path.endswith('!'))
