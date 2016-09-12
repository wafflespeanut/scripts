from datetime import datetime

import json, requests

# Basic CUI to interact with Asana tasks (my job demands using Asana, and I'm lazy!)

token = 'foobar123'
BASE_URL = 'https://app.asana.com/api/1.0'


def request(method, url, data=None):
    print '%s: %s' % (method, url)
    headers = {'Authorization': 'Bearer %s' % token}
    req_method = getattr(requests, method.lower())
    resp = req_method(url, data=data, headers=headers)
    obj = json.loads(resp.text)
    return obj['data'] if obj.get('data') else obj


def get_date():
    while True:
        try:
            date = raw_input('Due date in YYYY-MM-DD format (optional): ') or None
            if not date:
                return
            datetime.strptime(date, '%Y-%m')
            return date
        except ValueError as err:
            print 'Error: %s, Please try again...' % err


def get_task_data(user_id, space_id, proj_id):
    name = raw_input('Name of your task: ')
    if not name:
        return

    is_assigned = raw_input('Assign it to you (y/n)? ')
    due_date = get_date()
    is_complete = raw_input('Is it done (y/n)? ') == 'y'

    return {
        'name': name,
        'assignee': user_id if is_assigned == 'y' else None,
        'due_on': due_date,
        'completed': is_complete,
        'workspace': space_id,
        'projects': [proj_id]
    }


def get_input_for_opts(options, prompt, sort_key=None):
    options = sorted(options, key=sort_key)
    for i, opt in enumerate(options):
        val = sort_key(opt) if sort_key else opt
        print '%d. %s' % (i + 1, val)

    while True:
        try:
            string = raw_input('\n%s ' % prompt)
            if not string:
                return

            val = int(string)
            assert val >= 1, "value should be at least 1"
            assert val <= len(options), "value should be at most %s" % len(options)
            return options[val - 1] if sort_key else val - 1
        except Exception as err:
            print 'Error: %s, Please try again...' % err


# Recursively traverse through tasks, sub-tasks, sub-sub-tasks, etc.
def task_recursion(user_id, space_id, proj_id, task_id=None, level=0):
    print '\nTask recursion level: %d' % level
    task_url = '%s/tasks/%s/subtasks' % (BASE_URL, task_id)
    options = [
        'Assign this %stask to you' % ('sub-' * (level - 1)),
        'Set due date for this %stask' % ('sub-' * (level - 1)),
        'Mark this %stask as completed' % ('sub-' * (level - 1)),
        'Create a new %stask' % ('sub-' * level),
        'Update an existing %stask' % ('sub-' * level),
        '[Previous menu]'
    ]

    skip_first = 3
    if level == 0:
        options = options[skip_first:-1]
        task_url = '%s/projects/%s/tasks' % (BASE_URL, proj_id)

    while True:     # so that we can jump back to the previous menu (on null input)
        print
        idx = get_input_for_opts(options, 'Input:')
        if idx is None:
            print 'Returning to previous menu...'
            return

        idx += skip_first if level == 0 else 0

        if idx == 0:
            data = { 'assignee': 'me' }
            request('PUT', '%s/tasks/%s' % (BASE_URL, task_id), data)
            print 'Assigned!'

        elif idx == 1:
            date = get_date()
            if not date:
                return
            data = { 'due_on': date }
            request('PUT', '%s/tasks/%s' % (BASE_URL, task_id), data)
            print 'Due date changed!'

        elif idx == 2:
            data = { 'completed': True }
            request('PUT', '%s/tasks/%s' % (BASE_URL, task_id), data)

        elif idx == 3:
            data = get_task_data(user_id, space_id, proj_id)
            if not data:
                return

            request('POST', task_url, { 'data': data })

        elif idx == 4:
            print '[List of %stasks]' % ('sub-' * level)
            tasks = request('GET', task_url)
            if not tasks:
                print 'No %stasks found! Going back...' % ('sub-' * level)
                return

            task = get_input_for_opts(tasks,
                                      'Which %stask do you wanna interact with?' % ('sub-' * level),
                                      lambda v: v['name'])
            if not task:
                print 'Returning to previous menu...\n'
                continue

            print 'Task: %s' % task['name']
            task_recursion(user_id, space_id, proj_id, task['id'], level + 1)

        else:
            return


def begin_battle(space_id=None):
    user_id = request('GET', '%s/users/me' % BASE_URL)['id']
    print 'User ID: %s\n' % user_id

    if not space_id:
        workspaces = request('GET', '%s/workspaces' % BASE_URL)

        for space in workspaces:
            if 'genome' in space['name'].lower():
                space_id = space['id']
                print 'Workspace ID: %s\n' % space_id
                break

        if not space_id:
            exit('Workspace not found!\n')

    proj_url = '%s/projects' % BASE_URL
    projects = request('GET', proj_url)

    while True:
        print
        proj = get_input_for_opts(projects, 'Which project do you wanna interact with?',
                                  lambda v: v['name'])
        if not proj:
            return

        task_recursion(user_id, space_id, proj['id'])
