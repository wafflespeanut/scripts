from datetime import datetime

import json, requests

# Basic CUI to interact with Asana tasks (my job demands using Asana, and I'm lazy!)

token = 'foobar123'
BASE_URL = 'https://app.asana.com/api/1.0'


def request(method, url, data=None):
    print '%s: %s' % (method, url)
    headers = {'Authorization': 'Bearer %s' % token}
    if method == 'POST':
        headers['Content-type'] = 'application/json'
        data = json.dumps(data)

    req_method = getattr(requests, method.lower())
    resp = req_method(url, data=data, headers=headers)
    obj = json.loads(resp.text)
    return obj['data'] if obj.get('data') is not None else obj


def get_date():
    while True:
        try:
            date = raw_input("Due date in YYYY-MM-DD format (Press [Enter] for today, Press '!' to skip): ") or None
            if date == '!':
                return
            elif not date:
                return datetime.now().strftime('%Y-%m-%d')

            datetime.strptime(date, '%Y-%m-%d')
            return date
        except ValueError as err:
            print 'Error: %s, Please try again...' % err
        except KeyboardInterrupt:
            return


def get_task_data(space_id, proj_id):
    data = { 'workspace': space_id }
    if proj_id:
        data['projects'] = [proj_id]

    name = raw_input('Name of your task: ')
    if not name:
        return

    data['name'] = name
    is_assigned = raw_input('Assign it to you (y/n)? ') == 'y'
    if is_assigned:
        data['assignee'] = 'me'

    due_date = get_date()
    if due_date:
        data['due_on'] = due_date

    is_complete = raw_input('Is it done (y/n)? ') == 'y'
    if is_complete:
        data['completed'] = is_complete

    return data


def get_input_for_opts(options, prompt, sort_key=None, print_val=True):
    options = sorted(options, key=sort_key)
    for i, opt in enumerate(options):
        val = sort_key(opt) if sort_key and print_val else opt
        print '%d. %s' % (i + 1, val)

    while True:
        try:
            string = raw_input('\n%s ' % prompt)
            if not string:
                return

            val = int(string)
            assert val >= 1, "value should be at least 1"
            assert val <= len(options), "value should be at most %s" % len(options)
            return options[val - 1] if sort_key and print_val else val - 1
        except Exception as err:
            print 'Error: %s, Please try again...' % err
        except KeyboardInterrupt:
            print
            return


# Recursively traverse through tasks, sub-tasks, sub-sub-tasks, etc.
def task_recursion(space_id, proj_id, task={}, level=0):
    print '\n(Task recursion level: %d)' % level
    options = {
        'Assign this %stask to you' % ('sub-' * (level - 1)): 0,
        'Set due date for this %stask' % ('sub-' * (level - 1)): 1,
        'Mark this %stask as completed' % ('sub-' * (level - 1)): 2,
        'Rename this %stask' % ('sub-' * (level - 1)): 3,
        'Create a new %stask' % ('sub-' * level): 4,
        'Update an existing %stask' % ('sub-' * level): 5,
    }

    while True:     # so that we can jump back to the previous menu (on null input)
        task_id, task_name = task.get('id'), task.get('name')
        task_url = '%s/tasks/%s/subtasks' % (BASE_URL, task_id)
        skip_first = 4

        if level == 0:
            if task:
                task = {}
                continue

            options = dict(filter(lambda (_, v): v >= skip_first, options.items()))
            task_url = '%s/projects/%s/tasks' % (BASE_URL, proj_id)

        print ('Task: %s\n' % task_name) if task_name else ''
        idx = get_input_for_opts(options, 'Input:', options.get, print_val=False)
        if idx is None:
            print 'Returning to previous menu...'
            return

        idx += skip_first if level == 0 else 0

        if idx == 0:
            data = { 'assignee': 'me' }
            request('PUT', '%s/tasks/%s' % (BASE_URL, task_id), data)
            print 'Assigned to you!\n'

        elif idx == 1:
            date = get_date()
            if not date:
                return

            data = { 'due_on': date }
            request('PUT', '%s/tasks/%s' % (BASE_URL, task_id), data)
            print 'Due date changed!\n'

        elif idx == 2:
            data = { 'completed': True }
            request('PUT', '%s/tasks/%s' % (BASE_URL, task_id), data)
            print 'Marked as completed!\n'

        elif idx == 3:
            name = raw_input('Enter a new name for the %stask: ' % ('sub-' * (level - 1)))
            data = { 'name': name }
            request('PUT', '%s/tasks/%s' % (BASE_URL, task_id), data)
            print 'Renamed!\n'

        elif idx == 4:
            try:
                data = get_task_data(space_id, proj_id)
                if not data:
                    return
            except KeyboardInterrupt:
                return

            request('POST', task_url, { 'data': data })
            print 'Created new task!\n'

        elif idx == 5:
            print '\n[List of %stasks]' % ('sub-' * level)
            tasks = request('GET', task_url)
            if not tasks:
                raw_input('\nNo %stasks found! Press [Enter] to go back...' % ('sub-' * level))
                return

            while True:
                choice = get_input_for_opts(tasks,
                                            'Which %stask do you wanna interact with?' % ('sub-' * level),
                                            lambda v: v['name'])
                if not choice:
                    print 'Returning to previous menu...'
                    break

                task = choice
                task_recursion(space_id, None, task, level + 1)


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

        task_recursion(space_id, proj['id'])
