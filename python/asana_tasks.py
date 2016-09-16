from datetime import datetime
from time import sleep

import json, os, re, requests, sys

try:
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
except ImportError:
    exit('Requires selenium webdriver! Install it using %r' % 'pip install selenium')

CHROME_PATH = '/usr/lib/chromium-browser/chromedriver'

SAMPLE_CONFIG = {
    "token": "foobar123",
    "space": "genomels",

    "gnats_user": "ravishankar@genomels.com",
    "gnats_pass": 'SSdtIG5vdCB0aGF0IGR1bWIh'.decode('base64'),

    "tasks": {
        "YYYY-MM-DD": [
            {
                # "type" says what should be done for this group
                # "create-create" - create a new task and create a subtask
                # "update-create" - update an existing task and create a subtask
                # "update-update" - update an existing task and subtask
                # "custom" - create a custom task in gnats
                "type": "",
                "project": "",          # some project name (case insensitive)
                "task_name": "",        # some task name or pattern
                "task_assignee": "",    # (optional) assignee for new tasks (default: you)
                "task_date": "",        # (optional) due date for new tasks (default: null)

                "subtask": "",          # some subtask name (subtasks are always created)
                # (optional) due date for this subtask
                # (default: date you've mentioned above, for this task group)
                "subtask_date": "",
                "subtask_assignee": "", # (optional) assignee for subtasks (default: you)

                "hours": "",            # hours taken for this task
                # (optional) bool for "completed" (defaults to True)
                # (which marks the subtask as completed once we update it in Gnats)
                "completed": False,
            }
        ]
    }
}


def try_parse_datetime(dt, dt_format='%Y-%m-%d'):
    try:
        return datetime.strptime(dt, dt_format).strftime(dt_format)
    except ValueError:
        return None


class AsanaTasksCreator(object):
    '''
    Basic methods to interact with Asana tasks
    (my workplace demands using Asana for logging, and I'm lazy!)
    '''
    base_url = 'https://app.asana.com/api/1.0/'
    proj_url = '/projects'
    spaces_url = '/workspaces'
    users_url = '/workspaces/%s/users'
    tasks_url = '/tasks/%s'
    root_tasks_url = '/projects/%s/tasks'
    sub_tasks_url = '/tasks/%s/subtasks'

    def __init__(self, token):
        self.token = token

    def _request(self, method, rel_url, data=None):
        url = self.base_url + rel_url.lstrip('/')
        print '%s: %s' % (method, url)
        headers = {'Authorization': 'Bearer %s' % self.token}
        if method == 'POST':
            headers['Content-type'] = 'application/json'
            data = json.dumps(data)

        req_method = getattr(requests, method.lower())
        resp = req_method(url, data=data, headers=headers)
        obj = json.loads(resp.text)
        return obj['data'] if obj.get('data') is not None else obj

    def _get_stuff(self, url):
        stuff = {}
        for thing in self._request('GET', url):
            stuff[thing['name']] = thing['id']
        return stuff

    def get_workspaces(self):
        return self._get_stuff(self.spaces_url)

    def get_projects(self):
        return self._get_stuff(self.proj_url)

    def get_users(self, space_id):
        return self._get_stuff(self.users_url % space_id)

    def get_tasks(self, parent_id, is_root=False):
        url = self.root_tasks_url if is_root else self.sub_tasks_url
        return self._get_stuff(url % parent_id)

    def create_task_data(self, **kwargs):
        data = {}
        if kwargs.get('space_id'):
            data['workspace'] = kwargs['space_id']
        if kwargs.get('proj_id'):
            data['projects'] = [kwargs['proj_id']]
        if kwargs.get('name'):
            data['name'] = kwargs['name']
        if kwargs.get('assignee'):
            data['assignee'] = kwargs['assignee']
        if kwargs.get('completed'):
            data['completed'] = kwargs['completed']
        if kwargs.get('date') and try_parse_datetime(kwargs['date']):
            data['due_on'] = kwargs['date']
        return data

    def update_task(self, task_id, is_root=False, **kwargs):
        data = self.create_task_data(**kwargs)
        if not data:
            return

        self._request('PUT', self.tasks_url % task_id, data)

    def create_new_task(self, parent_id, is_root=False, **kwargs):
        if not (kwargs.get('name') and kwargs.get('space_id')):
            print 'WARNING: Name and Workspace IDs are required!'
            return

        if is_root:
            kwargs['proj_id'] = parent_id

        data = self.create_task_data(**kwargs)
        url = self.root_tasks_url if is_root else self.sub_tasks_url
        return self._request('POST', url % parent_id, {'data': data})

    def delete_task(self, task_id):
        self._request('DELETE', self.tasks_url % task_id)


class GnatsFiller(object):
    '''Selenium-based automation to get around my company's time tracker thing'''
    def __init__(self, username=None, password=None):
        self.driver = webdriver.Chrome(CHROME_PATH)
        self.driver.get("http://gnats.genomels.com/")
        if username:
            self.driver.find_element_by_xpath("//input[@id='user']").send_keys(username)
        if password:
            self.driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
        if username and password:
            self.driver.find_element_by_xpath("//button[@type='submit']").click()

        while not (username and password):
            raw_input('Continue after logging in...')
            if 'GLS Time Tracker' in self.driver.title:
                break

    def switch_to_date(self, date):
        date_url = 'http://gnats.genomels.com/ts_asana.php?tdate=%s' % date
        self.driver.get(date_url)

    def loop_wait(self, func):
        for i in xrange(1, sys.maxint):     # We won't usually go that far!
            try:
                func()
                print '\nFinished!'
                break
            except NoSuchElementException:
                sys.stdout.write('\rWaiting for page to finish loading... %d' % i)
                sys.stdout.flush()
                sleep(1)

    def list_tasks(self, proj_id):
        def inner():
            self.driver.find_element_by_xpath("//a[contains(.,'GNA - Prod Dev')]").click()
            sleep(1)
            self.driver.find_element_by_xpath("//a[contains(@id,'%s')]" % proj_id).click()
            # open additional tasks (without due-dates)
            self.driver.find_element_by_xpath("/html/body/div[2]/aside[2]/section[2]/div/div[1]/div[2]/div[1]/div/button").click()

        self.loop_wait(inner)

    def list_subtasks(self, task_name):
        def inner():
            td = self.driver.find_element_by_xpath("//td[contains(.,' %s')]" % task_name)
            tr = td.find_element_by_xpath('..')
            tr.find_element_by_tag_name('i').click()

        self.loop_wait(inner)

    def pick_subtask(self, subtask_name):
        def inner():
            td = self.driver.find_element_by_xpath("//td[contains(.,' %s')]" % subtask_name)
            tr = td.find_element_by_xpath('..')
            tr.find_element_by_tag_name('button').click()
            sleep(1)

        self.loop_wait(inner)

    def show_picked(self):
        self.driver.find_element_by_xpath("//button[@id='todays']").click()

    def custom_add(self, option, desc, hours):
        self.driver.find_element_by_xpath("//button[@id='addfield']").click()
        select = self.driver.find_element_by_xpath("//select[@name='category']")
        tr = select.find_element_by_xpath('../..')
        desc_inp = tr.find_element_by_xpath("//input[@name='descp']")
        desc_inp.send_keys(desc)
        hr_inp = tr.find_element_by_xpath("//input[@id='hours1']")
        hr_inp.send_keys(hours)

        options = select.find_elements_by_tag_name('option')
        chosen_opt = filter(lambda opt: re.search(option.lower(), opt.get_attribute('value').lower()), options)
        assert chosen_opt
        chosen_opt[0].click()

    def fill_picked(self, subtask_name, hours):
        def inner():
            td = self.driver.find_element_by_xpath("//td[contains(.,'%s')]" % subtask_name)
            tr = td.find_element_by_xpath('..')
            dt_hrs = try_parse_datetime(hours, '%H:%M')
            if not dt_hrs:
                print 'Unable to parse datetime (%s)' % hours
                dt_hrs = '00:00'
            tr.find_element_by_tag_name('input').send_keys(dt_hrs)

        self.loop_wait(inner)

    def update_filled(self):
        self.driver.find_element_by_xpath("//button[@id='addupdate']").click()

    def finish(self, expect_hours='09:00'):
        def inner():
            total_hours = self.driver.find_element_by_xpath("//center[@id='total_hours']").text
            dt_hrs = datetime.strptime(total_hours, '%H:%M')
            if dt_hrs < expect:
                if raw_input('WARNING: Expected hours (%s) not fulfilled! Continue (y/n)? ' % expect) == 'y':
                    raise StopIteration

        self.update_filled()
        expect = datetime.strptime(expect_hours, '%H:%M')
        self.loop_wait(inner)


def begin_battle(config):
    if not os.path.exists(CHROME_PATH):
        print 'Requires Chromedriver! Get it using %r' % 'sudo apt-get install chromium-chromedriver'
        return

    asana = AsanaTasksCreator(config['token'])
    space = config['space']

    if isinstance(space, str):
        spaces = asana.get_workspaces()
        spaces = filter(lambda (name, sp): re.search(config['space'], name), spaces.items())
        if not spaces:
            print 'Workspace not found!'
            return
        space = spaces[0][1]

    print 'Workspace ID: %d' % space
    fill_tasks = config['tasks']
    projects = {}

    # get the projects mentioned in the config
    for dt, tasks in fill_tasks.items():
        for task in tasks:
            if task.get('project'):
                proj = task['project'].lower()
                task['project'] = proj
                projects[proj] = {}

    # get the tasks corresponding to those projects
    for proj_name, proj_id in asana.get_projects().items():
        proj = proj_name.lower()
        if projects.get(proj) is not None:
            projects[proj]['id'] = proj_id
            projects[proj]['tasks'] = asana.get_tasks(proj_id, is_root=True)

    # start the driver
    username = config.get('gnats_user')
    password = config.get('gnats_pass')
    gnats = GnatsFiller(username, password)

    # Main loop
    for date, tasks_info in fill_tasks.items():
        date = try_parse_datetime(date)
        if not date:
            print 'Error parsing date: %r. Skipping task group...' % date
            continue

        tasks = []
        asana_tasks = []
        custom_tasks = []

        for task in tasks_info:
            if not try_parse_datetime(task['hours'], '%H:%M'):
                print 'Unable to parse hours (%s). Skipping %r...' % (task['hours'], task['subtask'])
                continue

            if task['type'] == 'custom':
                custom_tasks.append(task)
                continue

            proj = task['project']
            if not projects.get(proj):
                print 'Project %r not found in Asana! Skipping %r...' % (proj, task['subtask'])
                continue

            if task['type'] in ['update-create', 'create-create', 'update-update']:
                asana_tasks.append(task)
            else:
                print "Task handling for %r has not been implemented! Skipping %r..." % \
                    (task['type'], task['subtask'])

        for task in asana_tasks:
            created = []
            proj = projects[task['project']]
            task_name_or_pattern = task['task_name']
            task_type, subtask_type = task['type'].split('-')
            task_id = None

            if task_type == 'create':
                created = asana.create_new_task(parent_id=proj['id'], space_id=space,
                                                is_root=True, name=task_name_or_pattern,
                                                assignee=task.get('task_assignee', 'me'),
                                                date=try_parse_datetime(task.get('task_date')))
                task_id, task_name = created['id'], task_name_or_pattern
                proj['tasks'][task_name_or_pattern] = task_id
                print 'Created new task: %r' % task_name
                created.append(task_id)

            elif task_type == 'update':
                found = filter(lambda (name, _): re.search(task_name_or_pattern, name),
                               proj['tasks'].items())
                if not found:
                    print 'No matching tasks found! Skipping %r...' % task_name_or_pattern
                    continue

                task_name, task_id = found[0]
                print 'Task matched: %r' % task_name
                asana.update_task(task_id, assignee=task.get('task_assignee'), date=task.get('task_date'))

            subtask_name = task['subtask']
            subtask_id = None

            if subtask_type == 'create':
                print 'Creating new subtask %r...' % subtask_name
                sub_task = asana.create_new_task(parent_id=task_id, space_id=space,
                                                 name=subtask_name,
                                                 assignee=task.get('subtask_assignee', 'me'),
                                                 date=task.get('subtask_date'))
                subtask_id = sub_task['id']
                created.append(subtask_id)

            elif subtask_type == 'update':
                subtasks = asana.get_tasks(task_id)
                found = filter(lambda (name, _): re.search(subtask_name, name),
                               subtasks.items())
                if not found:
                    print 'No matching sub-tasks found! Skipping %r...'
                    continue

                subtask_name, subtask_id = found[0]
                print 'Sub-task matched: %r' % subtask_name
                asana.update_task(subtask_id,
                                  assignee=task.get('subtask_assignee'),
                                  date=task.get('subtask_date'))

            gnats.switch_to_date(date)
            gnats.list_tasks(proj['id'])
            gnats.list_subtasks(task_name)
            gnats.pick_subtask(subtask_name)
            gnats.show_picked()
            gnats.fill_picked(subtask_name, task['hours'])
            gnats.update_filled()

            if task.get('completed', True):
                asana.update_task(subtask_id, completed=True)
                print 'Marked %r as completed!' % subtask_name

            # FIXME: delete created tasks (and unpick them) on exception

        for task in custom_tasks:
            print 'Adding custom task... %r' % task['subtask']
            gnats.show_picked()
            gnats.custom_add(task['task_name'], task['subtask'], task['hours'])
            gnats.update_filled()


    sleep(5)
    gnats.driver.close()
