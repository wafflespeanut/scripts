import inspect, os, sys

# for https://bugzilla.mozilla.org/show_bug.cgi?id=1277133
# (just to automate some fixes which we're absolutely sure about, and too lazy to do those!)

filename = inspect.getframeinfo(inspect.currentframe()).filename
exec_path = os.path.dirname(os.path.abspath(filename))
execfile(os.path.join(exec_path, 'helpers.py'))     # for safely executing a commmand

PATH = '/media/Windows/Mozilla/mozilla-central/'
CONSTS = os.path.join(PATH, 'layout', 'style', 'nsStyleConsts.h')
PREFIX = 'NS_STYLE_'


def left_trim(string, sub):     # helper
    return string[len(sub):] if string.startswith(sub) else string


def parse_const(line):      # try to parse a line containing the constant (allowing errors to bubble, if any)
    stripped = left_trim(line, '#define').strip()
    stuff = iter(stripped.split())
    name, value = stuff.next(), int(stuff.next())

    try:
        return name, value, stuff.next()
    except StopIteration:
        return name, value, ''


def find_constant(contents, idx = 0):       # find first matching constant
    for (i, line) in enumerate(contents[idx:]):
        const = left_trim(line, '#define').strip()
        if not const.startswith(PREFIX):
            continue

        if const.startswith(const_upper):
            print '\nBreaking on first matching line: %d' % (idx + i + 1)
            return idx + i

# Constants are mostly grouped with incrementally occurring integers
# (here, we find such a group by setting its boundaries)
def find_boundary(contents, idx, reverse = False):      # works only for integers
    i = idx
    try:
        _n, prev_val, _c = parse_const(contents[i])

        if reverse:
            while i > 0 and contents[i - 1].startswith('#define'):
                _n, cur_val, _c = parse_const(contents[i - 1])
                if cur_val >= prev_val:
                    break

                prev_val = cur_val
                i -= 1
        else:
            while i < len(contents) - 1 and contents[i + 1].startswith('#define'):
                _n, cur_val, _c = parse_const(contents[i + 1])
                if cur_val <= prev_val:
                    break

                prev_val = cur_val
                i += 1
            i += 1
        return i
    except ValueError:
        raise ValueError, i if reverse else i + 2


def collect_all(contents, prefix, idx = 0):     # get all the constants
    lines, consts = [], []
    for i, line in enumerate(contents[idx:]):
        if line.startswith('#define'):
            stripped = left_trim(line, '#define').strip()
            if stripped.startswith(prefix):
                try:
                    consts.append(parse_const(line))
                except ValueError:
                    pass
                lines.append(idx + i)
    return lines, consts


if __name__ == '__main__':
    os.chdir(PATH)
    args = sys.argv[1:]
    if not args:
        exit('\nRequires a constant group')

    const_group = '_'.join(args)
    const_upper = const_group.upper()
    if not const_upper.startswith(PREFIX):
        const_upper = PREFIX + const_upper

    with open(CONSTS, 'r') as fd:
        contents = fd.readlines()

    found = find_constant(contents)
    if not found:
        exit('\nConstant group not found in file!')

    try:
        start_idx = find_boundary(contents, found, reverse = True)
        end_idx = find_boundary(contents, found)
        print "Grouped constants in range(%s:%s)\n" % (start_idx, end_idx)
        print ''.join(contents[start_idx:end_idx])
    except ValueError as i:
        exit('Error parsing line %s: This currently works only for integer constants!' % i)

    # 'word counting' based scheme for collecting the repetitively occurring prefixes
    # and forming an enum class name out of them
    const_stuff = map(parse_const, contents[start_idx:end_idx])
    const_list = map(lambda (name, _val, _c): name, const_stuff)
    counts = reduce(lambda d1, d2: dict((s, d1.get(s, 0) + d2.get(s, 0)) for s in set(d1).union(set(d2))),
                    map(lambda name: dict((word, 1) for word in name.split('_')), const_list))
    max_count = max(counts.values())

    names = filter(lambda word: counts[word] == max_count, const_list[0].split('_'))
    enum_class_name = ''.join(map(str.title, names[1:]))
    print 'Predicted enum class name: %r' % enum_class_name
    print 'Searching for similar constants...'

    prefix = '_'.join(names)
    lines, more_consts = collect_all(contents, prefix, end_idx)
    if more_consts:     # FIXME (could be fixed if the intermediate lines are only comments)
        print '\n%d constants have been found with the same prefix!' % len(lines)
        exit("It's not safe to run this script on these cases...")
