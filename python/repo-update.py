import inspect, os

filename = inspect.getframeinfo(inspect.currentframe()).filename
exec_path = os.path.dirname(os.path.abspath(filename))
execfile(os.path.join(exec_path, 'helpers.py'))

PARENT_DIRS = ['/media/Ubuntu']


class Repo(object):
    def __init__(self, dirname):
        print '\n\033[92mSwitching to %s...\033[0m' % dirname
        os.chdir(dirname)
        self.check()
        self.merge()


class Git(Repo):
    def __init__(self, dirname):
        super(Git, self).__init__(dirname)

    def check(self):
        out = exec_cmd('git branch')
        if 'master' not in out:
            raise Exception("'master' branch unavailable! Getting out...")
        idx = out.find('*')
        if not out[idx:].startswith('* master'):
            print 'This looks like another branch. Trying to checkout to master...'
            out = exec_cmd('git checkout master')
            if 'Switched to branch' not in out:
                raise Exception('Unable to switch branch!')

    def merge(self):
        out = exec_cmd('git fetch upstream', prefer_lines=False)
        if 'fatal' in out:
            raise Exception("Unable to fetch from 'upstream'!")
        exec_cmd('git merge upstream/master', needs_output=False, prefer_lines=False)


class Hg(Repo):
    def __init__(self, dirname):
        super(Hg, self).__init__(dirname)

    def check(self):
        print 'Popping all patches from queue...'
        exec_cmd('hg qpop -a', needs_output=False)

    def merge(self):
        out = exec_cmd('hg pull -u', prefer_lines=False)
        if 'abort' in out:
            raise Exception('Merging failed!')


if __name__ == '__main__':
    for parent_dir in PARENT_DIRS:
        for repo in os.listdir(parent_dir):
            try:
                abs_path = os.path.join(parent_dir, repo)
                instance = None
                if os.path.exists(os.path.join(abs_path, '.git')):
                    instance = Git
                elif os.path.exists(os.path.join(abs_path, '.hg')):
                    instance = Hg
                if instance is None:
                    raise Exception("%s is not a 'git' or 'hg' repo! Getting out..." % abs_path)
                instance(abs_path)
            except KeyboardInterrupt:
                exit('Interrupted!')
            except Exception as err:
                print '\n\033[91m%s\033[0m' % err
