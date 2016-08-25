from time import sleep
import inspect, os, sys

# for https://bugzilla.mozilla.org/show_bug.cgi?id=1277133
# (just to automate some fixes which we're absolutely sure about, and too lazy to do those!)

filename = inspect.getframeinfo(inspect.currentframe()).filename
exec_path = os.path.dirname(os.path.abspath(filename))
execfile(os.path.join(exec_path, 'helpers.py'))     # for safely executing a commmand

PATH = '/media/Windows/Mozilla/mozilla-central/'

CONSTS_REL_PATH = os.path.join('layout', 'style', 'nsStyleConsts.h')
PREFIX_NAMES = []       # something like ['NS', 'STYLE']
PREFIX = '_'.join(PREFIX_NAMES)
TAB_LEN = 2
PREFER_UNDERSCORES = ['None']
SCRAPE_SLEEP_TIMEOUT = 5


def left_trim(string, sub):
    return string[len(sub):] if string.startswith(sub) else string


def parse_const(line):      # try to parse a line containing the constant (allowing errors to bubble, if any)
    global_names = globals()
    stripped = left_trim(line, '#define').strip()
    comment_idx = stripped.find('//')
    comment = ''

    if comment_idx > 0:
        comment = stripped[comment_idx:]
        stripped = stripped[:comment_idx] + '#' + comment

    stuff = stripped.split()
    name = stuff.pop(0)
    value = ' '.join(word for word in stuff)
    # magic to evaluate RHS and put it into the global namespace
    exec '%s = %s' % (name, value) in global_names
    return name, global_names[name], comment


def find_constant(prefix, contents, idx = 0):       # find first matching constant
    for (i, line) in enumerate(contents[idx:]):
        if not line.startswith('#define'):
            continue

        try:    # store all the previous constants in the namespace
            const, _, _ = parse_const(line)
        except:
            continue

        if const.startswith(prefix):
            print 'Breaking on first matching line: %d\n' % (idx + i + 1)
            return idx + i

# Constants are mostly grouped with incrementally occurring integers
# (here, we find such a group by setting its boundaries)
def find_boundary(file_contents, idx, reverse = False):
    contents = file_contents[::-1] if reverse else file_contents
    i = len(contents) - idx - 1 if reverse else idx
    _n, prev_val, _c = parse_const(contents[i])
    check = (lambda cur, prev: cur >= prev) if reverse else lambda cur, prev: cur <= prev

    while i < len(contents) - 1 and contents[i + 1].startswith('#define'):
        i += 1
        _n, cur_val, _c = parse_const(contents[i])
        if cur_val <= prev_val:
            return i
        prev_val = cur_val
    return len(contents) - i - 1 if reverse else i + 1


def collect_all(contents, prefix, idx = 0):     # get all the line indices containing the constants
    indices = []
    for i, line in enumerate(contents[idx:]):
        if line.startswith('#define'):
            stripped = left_trim(line, '#define').strip()
            if stripped.startswith(prefix):
                indices.append(idx + i)
    return indices


if __name__ == '__main__':
    os.chdir(PATH)
    simulate = True
    is_offline = True
    const_group = map(str.upper, '_'.join(sys.argv[1:]).split('_'))

    try:
        execfile(os.path.join(exec_path, 'dxr_grep.py'))
        is_offline = False
    except ImportError:
        print "'dryscraper' module not found! Falling back to offline 'grep'ing..."

    try:
        idx = const_group.index('-W')
        const_group.pop(idx)
        simulate = False
    except ValueError:
        print "\033[93m\033[1mSimulating actual process (pass '-w' to override)...\033[0m"

    if not const_group:
        exit('\nRequires a constant group')

    # neglect 'ns' or 'style' stuff present (if any) - we'll prepend those later
    for word in PREFIX_NAMES:
        if word == const_group[0]:
            const_group.pop(0)
    const_upper = '_'.join(const_group)

    if not const_upper.startswith(PREFIX):
        const_upper = PREFIX + '_' + const_upper

    with open(CONSTS_REL_PATH, 'rb') as fd:
        contents = fd.readlines()

    print '\nLooking for %s*...' % const_upper
    found = find_constant(const_upper, contents)
    if not found:
        exit('Constant group not found in file!')

    try:
        print 'Isolating the group...'
        start_idx = find_boundary(contents, found, reverse = True)
        end_idx = find_boundary(contents, found)
        stuff = contents[start_idx:end_idx]
        assert len(stuff) > 1, "The script won't do any good for a group containing single constant!"
        print ''.join(['%d:\t%s' % (start_idx + i + 1, line) for i, line in enumerate(stuff)])
    except AssertionError as err:
        exit(err)

    # 'word counting' based scheme for collecting the repetitively occurring prefixes
    # and forming an enum class name out of them
    const_stuff = map(parse_const, stuff)
    const_list = map(lambda (name, _val, _c): name, const_stuff)
    counts = reduce(lambda d1, d2: dict((s, d1.get(s, 0) + d2.get(s, 0)) for s in set(d1).union(set(d2))),
                    map(lambda name: dict((word, 1) for word in name.split('_')), const_list))
    max_count = max(counts.values())

    names = filter(lambda word: counts[word] == max_count, const_list[0].split('_'))
    enum_class_name = ''.join(map(str.title, names[1:]))        # ignore 'NS_' prefix
    print 'Predicted enum class name: %r' % enum_class_name
    print 'Searching for similar constants...'
    prefix = '_'.join(names)

    def collect_and_try_parsing(contents, end_idx):
        indices = collect_all(contents, prefix, end_idx)
        if indices:
            # check whether the intermediate lines are comments (and proceed only if they are)
            for idx in range(end_idx, indices[-1] + 1):
                line = contents[idx]
                stripped = line.strip()
                if not stripped:
                    continue
                elif line.startswith('//'):
                    name, val, comment = const_stuff[-1]
                    const_stuff[-1] = name, val, comment + '\n' + ' ' * TAB_LEN + stripped
                elif idx in indices:
                    const = parse_const(line)
                    const_stuff.append(const)
                else:
                    print '\n%d more constants have been found with the same prefix! (lines: %s)' \
                          % (len(indices), ', '.join(map(lambda i: str(i + 1), indices)))
                    exit("It's not safe to run this script in these cases...")

            print 'Found %d more (and updated the list!)' % len(indices)


    collect_and_try_parsing(contents, end_idx)
    enum = ['enum class %s : uint8_t {' % enum_class_name]
    filter_prefix = '_'.join(map(str.upper, names)) + '_'
    variants, replacements = [], {}
    max_len = 0
    prev_val = const_stuff[0][1] - 1

    # format the variants appropriately
    for name, val, comment in const_stuff:
        variant = ''.join(map(str.title, left_trim(name, filter_prefix).split('_')))
        variant += '_' if variant in PREFER_UNDERSCORES else ''
        replacements[name] = '%s::%s' % (enum_class_name, variant)
        line = '  %s,' % variant if val == prev_val + 1 else '  %s = %d,' % (variant, val)
        variants.append((line, comment))
        prev_val = val
        if comment and len(line) > max_len:     # figure out comment position
            max_len = len(line)

    cmt_sep = TAB_LEN + max_len % TAB_LEN
    enum.extend(['%s%s' % (var, (max_len - len(var) + cmt_sep) * ' ' + cmt if cmt else '') for var, cmt in variants])
    enum.append('};\n')
    replace_enum = '\n'.join(enum)
    print '\n[Replacement enum]'
    print replace_enum

    contents[start_idx:end_idx] = [replace_enum]
    print 'Replacement map for constants:'
    for c, v in replacements.items():
        print '%s -> %s' % (c, v)

    if raw_input('\nContinue with replacement (y/n)? ') != 'y':
        exit()


    def parse_grepped(line):    # replace the constant with enum variant in grepped line
        split = iter(line.split(':'))
        rel_path = split.next()
        if rel_path == CONSTS_REL_PATH:
            return

        _rev = split.next()
        line_num = int(split.next())
        line = ':'.join([thing for thing in split])

        for const in replacements:
            if const in line:       # so that we filter only those variants we want
                print '%s:%d: %s' % (rel_path, line_num, line.rstrip())
                if files.get(rel_path):
                    files[rel_path].append(line_num)
                else:
                    files[rel_path] = [line_num]
                break       # one match is enough

    def check_files(files):     # because local and remote repos could be at different revisions
        modified = {}
        for rel_path in files:
            if rel_path == CONSTS_REL_PATH:
                continue

            modified[rel_path] = []
            with open(rel_path, 'r') as fd:     # FIXME: inefficient! (wrote it to comply with the other function)
                for i, line in enumerate(fd.readlines()):
                    for const in replacements:
                        if const in line:
                            print '%s:%d: %s' % (rel_path, i + 1, line.strip())
                            modified[rel_path].append(i + 1)
                            break
        return modified


    files = {}

    try:        # go for DXR
        files, all_found = search_dxr(prefix, print_results = False)
        files = check_files(files)
    except KeyboardInterrupt:
        pass
    except:     # fall back to the good ol' days...
        is_offline = True

    if is_offline:
        try:    # default grep
            command = "hg grep -n '%s'" % prefix
            print "\nCollecting files to be modified... (Press 'Ctrl-C' to interrupt)"
            exec_cmd(command, parse_grepped)
        except KeyboardInterrupt:
            pass

    if not files:
        exit('No changes to be made!')

    if raw_input('\n%d file(s) could be modified! Continue (y/n)? ' % len(files)) == 'y':
        for path in files:
            print "\nModifying '%s'..." % path
            with open(path, 'rb') as fd:
                lines = fd.readlines()

            for line_num in files[path]:
                idx = line_num - 1
                old_line = lines[idx]

                for const, variant in replacements.items():
                    if path.endswith('.h'):
                        variant = 'mozilla::%s' % variant
                    lines[idx] = lines[idx].replace(const, variant)
                print '%d: %s \033[91m\033[1m=>\033[0m %s' % (line_num, old_line.strip(), lines[idx].strip())

            if not simulate:
                with open(path, 'wb') as fd:
                    fd.writelines(lines)

        if not simulate:
            with open(CONSTS_REL_PATH, 'wb') as fd:
                fd.writelines(contents)
        print '\nConstants in %r have been replaced with the respective enum class!' % CONSTS_REL_PATH

        print '\nFile changes have been made!'
        print "The build won't probably succeed, since this script replaces only the directly visible constants."
        print 'Please run `./mach build` and fix the errors (if any)...'
