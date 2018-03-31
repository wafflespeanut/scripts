from collections import OrderedDict
from datetime import datetime

import inspect, json, os, subprocess, re, sys, uuid

currentPath = os.path.abspath('.')
WORKING_FILE = os.path.join(currentPath, 'COMMITS.json')

def execGitCmd(cmd, shell=False, env=os.environ):
    handle = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, env=env)
    code = handle.wait()
    out, err = handle.communicate()
    return out, err, code

# Find Git repo

repoFound = False
args = sys.argv[1:]
if args:
    path = os.path.expanduser(args[0])
    if not os.path.exists(path):
        exit('No such path')

    os.chdir(path)
    out, err, code = execGitCmd(['git', 'status'])
    if code is 0:
        repoFound = True
    if 'clean' not in out:
        exit('The repository is not clean. Please commit/stash your changes before continuing...')

if not repoFound:
    exit('Please specify a git repository')

# Get branch

branch = out.split('\n')[0].split()[-1]

# Pick base commit

out, err, code = execGitCmd(['git', 'log', '--merges', '-n1', '--format=%H'])
baseCommit = out.strip()
if baseCommit:
    print 'Choosing commits since merge %s' % baseCommit
else:
    out, err, code = execGitCmd('git log --reverse --format=%H | head -1', shell=True)
    baseCommit = out.strip()
    print 'No merge has been made. Choosing first commit: %s' % baseCommit

# Get all commits from base

out, err, code = execGitCmd(['git', 'log', baseCommit + '..', '--format=%H'])
commits = out.strip().split('\n')
if not commits or not commits[0]:
    exit('No commits found since the last merge.')

print 'Collecting %s commits from branch %s...' % (len(commits), branch)
commitData = OrderedDict()      # Order is necessary

for commit in commits:
    out, err, code = execGitCmd(['git', 'show', commit, '--no-patch'])
    match = re.match('commit %s\nAuthor:[ ]*(.*)\nDate:[ ]*(.*)\n\n(.*)' % commit, out, re.DOTALL)
    author = match.group(1)
    date = match.group(2)
    date, tzinfo = datetime.strptime(date[:-6], '%a %b %d %H:%M:%S %Y'), date[-5:]
    message = '\n'.join(map(lambda line: line[4:], match.group(3).rstrip().split('\n')))
    commitData[commit] = json.loads(json.dumps({
        'author': author,
        'date': date.strftime('%Y-%m-%d %T') + ' ' + tzinfo,
        'message': message
    }))

# Dump it to file

with open(WORKING_FILE, 'w') as fd:
    json.dump(commitData, fd, indent=2)

raw_input('Written to %s. Continue after making changes...' % WORKING_FILE)

# Load new commit data

randomBranch = uuid.uuid4().hex
branchBase = baseCommit

while True:
    with open(WORKING_FILE, 'r') as fd:
        try:
            newCommitData = json.load(fd)

            # Find the first commit whose data has been changed (actually, we need its parent).
            # Because, there's no reason to change the commits which don't need to be changed.
            # Also validate the changed data along the way.

            for (i, commit) in enumerate(reversed(commits)):
                data = newCommitData.get(commit)
                if data is None or not data.get('author') or not data.get('date') or not data.get('message'):
                    exit('Invalid commit data for %s. Exiting...' % commit)
                try:
                    date, tzinfo = datetime.strptime(data['date'][:-6], '%Y-%m-%d %H:%M:%S'), data['date'][-5:]
                    assert len(tzinfo) == 5 and tzinfo.startswith('+')
                except ValueError, AssertionError:
                    exit('Invalid date for commit %s. Exiting...' % commit)

                if data != commitData[commit]:
                    print 'Skipping %s commits (since metadata is unchanged)...' % i
                    break
                branchBase = commit

            out, err, code = execGitCmd(['git', 'checkout', '-b', randomBranch, branchBase])
            if code is 0:
                break

            print 'Error checking out to a temporary branch. Please commit/stash your changes before continuing...'
        except ValueError as err:
            print 'Error loading JSON file (%s). Please try again...' % err


print 'Warning! Do not make any changes in the repo.'

branchFound = branchBase == baseCommit      # Initial value
for commit in reversed(commits):
    if commit == branchBase:
        branchFound = True
        continue

    if branchFound:
        out, err, code = execGitCmd(['git', 'cherry-pick', commit])
        if code is not 0:
            execGitCmd(['git', 'checkout', branch])
            execGitCmd(['git', 'branch', '-D', randomBranch])
            exit('Error cherry picking commit.')

        env = os.environ.copy()
        data = newCommitData[commit]
        date, tzinfo = datetime.strptime(data['date'][:-6], '%Y-%m-%d %H:%M:%S'), data['date'][-5:]
        date = date.strftime('%a %b %d %H:%M:%S %Y') + ' ' + str(tzinfo)
        env['GIT_AUTHOR_DATE'] = date
        env['GIT_COMMITTER_DATE'] = date
        out, err, code = execGitCmd(['git', 'reset', '--soft', 'HEAD~1'])
        out, err, code = execGitCmd(['git', 'commit', '--author=%s' % data['author'], '-m', data['message']], env=env)
        if code is not 0:
            execGitCmd(['git', 'checkout', branch])
            execGitCmd(['git', 'branch', '-D', randomBranch])
            exit('Error amending commit.')

if raw_input('Rewritten commits. Do you want to remove the old branch? (y/n) ') == 'y':
    out, err, code = execGitCmd(['git', 'branch', '-D', branch])
    out, err, code = execGitCmd(['git', 'branch', '-m', branch])
else:
    out, err, code = execGitCmd(['git', 'checkout', branch])
    print ('\nIn that case, you may wanna `cd` into your repository and run '
           '`git checkout %s && git branch -D %s && git branch -m %s` (if you wanna '
           'switch to the rewritten version), or `git branch -D %s` (to remove the rewritten branch)') % (randomBranch, branch, branch, randomBranch)

os.remove(WORKING_FILE)
