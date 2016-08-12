import inspect, os, sys, subprocess

# for https://bugzilla.mozilla.org/show_bug.cgi?id=1277133
# (just to automate some fixes which we're absolutely sure about, and too lazy to do those!)

filename = inspect.getframeinfo(inspect.currentframe()).filename
exec_path = os.path.dirname(os.path.abspath(filename))
execfile(os.path.join(exec_path, 'helpers.py'))

PATH = '/media/Windows/Mozilla/mozilla-central/'
CONSTS = os.path.join(PATH, 'layout', 'style', 'nsStyleConsts.h')
PREFIX = 'NS_STYLE_'

os.chdir(PATH)
args = sys.argv[1:]
if not args:
    exit('\nRequires a constant group')

const_group = '_'.join(args)
const_upper = const_group.upper()
if not const_upper.startswith(PREFIX):
    const_upper = PREFIX + const_upper

def parse_const(line):
    stripped = line.lstrip('#define').lstrip().rstrip()
    stuff = iter(stripped.split())
    return stuff.next(), int(stuff.next())

def find_constant(contents, idx = 0):
    for (i, line) in enumerate(contents[idx:]):
        const = line.lstrip('#define').lstrip().rstrip()
        if not const.startswith(PREFIX):
            continue

        if const.startswith(const_upper):
            print '\nBreaking on first matching line: %d' % (idx + i + 1)
            return idx + i

def find_boundary(contents, idx, reverse = False):      # works for integers (for now)
    i = idx
    _name, prev_val = parse_const(contents[i])

    if reverse:
        while i > 0 and contents[i - 1].startswith('#define'):
            _name, cur_val = parse_const(contents[i - 1])
            if cur_val >= prev_val:
                break

            prev_val = cur_val
            i -= 1
    else:
        while i < len(contents) - 1 and contents[i + 1].startswith('#define'):
            _name, cur_val = parse_const(contents[i + 1])
            if cur_val <= prev_val:
                break

            prev_val = cur_val
            i += 1
    return i


with open(CONSTS, 'r') as fd:
    contents = fd.readlines()

found = find_constant(contents)
if not found:
    exit('\nConstant group not found in file!')

start_idx = find_boundary(contents, found, reverse = True)
end_idx = find_boundary(contents, found)
print "Grouped constants in range(%s:%s)\n" % (start_idx, end_idx)
print ''.join(contents[start_idx:(end_idx + 1)])

