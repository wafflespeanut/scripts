from datetime import datetime
from time import sleep

import json, os, re, requests, sys

try:
    from selenium import webdriver
    from selenium.common.exceptions import NoSuchElementException
except ImportError:
    exit('Requires selenium webdriver! Install it using %r' % 'pip install selenium')

CHROME_PATH = '/usr/lib/chromium-browser/chromedriver'


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

    def create_task_data(**kwargs):
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
        if kwargs.get('date'):
            date = datetime.strptime(kwargs['date'], '%Y-%m-%d')
            data['due_on'] = date.strftime('%Y-%m-%d')
        return data

    def update_task(self, task_id, is_root=False, **kwargs):
        data = self.create_task_data(**kwargs)
        if not data:
            return

        url = self.tasks_url % task_id
        self._request('PUT', task_id, data)

    def create_new_task(self, parent_id, is_root=False, **kwargs):
        if not (kwargs['name'] and kwargs['space_id']):
            return

        if is_root and not kwargs['proj_id']:
            return

        data = self.create_task_data(**kwargs)
        url = self.root_tasks_url if is_root else self.sub_tasks_url
        self._request('POST', url % parent_id, data)


class GnatsFiller(object):
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

    def switch_date(self, date):
        date_url = 'http://gnats.genomels.com/ts_asana.php?tdate=%s' % date
        self.driver.get(date_url)

    def loop_wait(self, func):
        for i in xrange(1, sys.maxint):     # We won't usually go that far!
            try:
                func()
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

    def add_custom(self, option, desc, hours):
        self.driver.find_element_by_xpath("//button[@id='addfield']").click()
        select = self.driver.find_element_by_xpath("//select[@name='category']")
        tr = select.find_element_by_xpath('../..')
        desc_inp = tr.find_element_by_xpath("//input[@name='descp']")
        desc_inp.send_keys(desc)
        hr_inp = tr.find_element_by_xpath("//input[@id='hours1']")
        hr_inp.send_keys(hours)

        options = select.find_elements_by_tag_name('option')
        chosen_opt = filter(lambda opt: opt.get_attribute('value').lower() == option.lower(), options)
        assert chosen_opt
        chosen_opt[0].click()

    def fill_picked(self, hours):
        td = self.driver.find_element_by_xpath("//td[contains(.,'%s')]" % subtask_name)
        tr = td.find_element_by_xpath('..')
        tr.find_element_by_tag_name('input').send_keys(hours)

    def finish(self, expect='09:00'):
        def inner():
            total_hours = self.driver.find_element_by_xpath("//center[@id='total_hours']").text
            dt_hrs = datetime.strptime(total_hours, '%H:%M')
            if dt_hrs < expect:
                if raw_input('WARNING: Expected hours (%s) not fulfilled! Continue (y/n)? ' % expect) == 'y':
                    raise StopIteration

        self.driver.find_element_by_xpath("//button[@id='addupdate']")
        expect = datetime.strptime(expect_hours, '%H:%M')
        self.loop_wait(inner)


def begin_battle(config):
    if not os.path.exists(CHROME_PATH):
        exit('Requires Chromedriver! Get it using %r' % 'sudo apt-get install chromium-chromedriver')

    api = AsanaTasksCreator(config['token'])
    space = config['space']

    if isinstance(space, str):
        spaces = api.get_workspaces()
        for name, space in spaces.items():
            if re.search(config['space'], name):
                break

    print 'Workspace ID: %d' % (space)
    projects = api.get_projects()
    tasks = config['tasks']

    # let the siege begin!
