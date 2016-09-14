from datetime import datetime

import json, re, requests


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


def begin_battle(config):
    api = AsanaTasksCreator(config['token'])
    space = config['space']

    if isinstance(space, str):
        spaces = api.get_workspaces()
        for name, space in spaces.items():
            if re.search(config['space'], name):
                break

    print 'Workspace ID: %d' % (space)
    projects = api.get_projects()

    for name, proj_inner in config['projects'].items():
        for proj_name, proj_id in projects.items():
            if name != proj_name:
                continue

            print 'Project: %s (ID: %d)' % (name, proj_id)
            update_tasks = proj_inner.get('UPDATE')
            if not update_tasks:
                continue

            tasks = api.get_tasks(proj_id, is_root=True)

            for pattern, task_inner in update_task.items():
                for task_name, task_id in tasks.items():
                    if not re.search(pattern, task_name):
                        continue

                    new_tasks = task_inner.get('NEW')
                    if not new_tasks:
                        continue

                    for subtask in new_tasks:
                        api.create_new_task(parent_id=task_id, space_id=space_id, **subtask)
                        print 'Task: %r created!' % subtask['name']

                        # invoke selenium

