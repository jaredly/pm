#!/usr/bin/env python
'''
Tasks have the following attributes:

    id:
    name
    created
    modified
    completed
    priority
    notes
    items []
'''

from parse_date import parse_datetime, time_fmt
import datetime
from yaml_block import block

class ParseError(Exception):
    '''Error parsing tasks'''
    def __str__(self):
        return "Error parsing yaml: %s" % self.message

def parse_id(text):
    if text.strip().isdigit():
        i = int(text)
        if i > 0:
            return i
    return 0

default_task = {'name': '', 'id': 0, 'created': None,
        'modified': None, 'completed': None, 'items': None, 'notes': None}

def new_task(news={}):
    task = default_task.copy()
    task['items'] = []
    task.update(news)
    return task

def dates_dct(today):
    return {'today': today,
            'yesterday': today + datetime.timedelta(-1),
            'tomorrow': today + datetime.timedelta(1)}

def inflate_date(text, dates, default):
    if text in dates:
        return dates[text]
    elif not text or not text.strip():
        return default
    date = parse_datetime(text, dates['today'])
    if not date:
        return default
    return date

def inflate_task(dct, today):
    task = new_task(dct)
    task['items'] = [inflate_task(item, today) for item in task['items']]
    dates = dates_dct(today)
    task['created'] = inflate_date(task['created'], dates, today)
    task['modified'] = inflate_date(task['modified'], dates, today)
    task['completed'] = inflate_date(task['completed'], dates, None)
    return task

def collapse_string(task):
    return '{name}|{id}|{created}|{modified}|{completed}'.format(**task)

def expand_string(text, today):
    '''A collapsed string looks like "title|id|created|modified|completed"'''
    if not text.strip():
        return None
    parts = map(str.strip, text.split('|'))
    data = {'name': parts[0]}
    if len(parts) > 1:
        data['id'] = parse_id(parts[1])
    if len(parts) > 2:
        data['created'] = parse_datetime(parts[2], today)
    if len(parts) > 3:
        data['modified'] = parse_datetime(parts[3], today)
    if len(parts) > 4:
        data['completed'] = parse_datetime(parts[4], today)
    if data.get('created', None) is None:
        data['created'] = today
    if data.get('modified', None) is None:
        data['modified'] = today
    return new_task(data)

class TaskMap:
    '''This handles all of the task parsing.'''
    def __init__(self, raw, today):
        self.tmap = {}
        self.tasks = []
        self.unassigneds = {}
        self.unassigned = 0
        self.max = 0
        self.today = today
        self.tasks = self.process_subtasks(raw)
        self.reassign()

    def reassign(self):
        for i in xrange(1, self.unassigned + 1):
            self.unassigneds[i]['id'] = self.max + i
        self.max += self.unassigned
        self.unassigned = 0
        self.unassigneds = {}

    def unassign(self, task):
        self.unassigned += 1
        self.unassigneds[self.unassigned] = task
        task['id'] = -self.unassigned

    def process_id(self, task):
        if task['id'] <= 0:
            self.unassign(task)
        elif task['id'] > self.max:
            self.max = task['id']

    def add_task(self, title, body):
        task = expand_string(title, self.today)
        self.process_id(task)
        if body:
            self.process_body(body, task)
        return task

    def process_subtasks(self, raw):
        '''Take the raw items, turn them into tasks'''
        tasklist = []
        if type(raw) == dict:
            for name, body in sorted(raw.iteritems()):
                # body [ list | dict ]
                tasklist.append(self.add_task(name, body))
        elif type(raw) in (list, tuple):
            for item in raw:
                if type(item) == str:
                    tasklist.append(self.add_task(item, None))
                elif type(item) == dict:
                    if len(item) == 1:
                        k = item.keys()[0]
                        tasklist.append(self.add_task(k, item[k]))
                    else:
                        print 'Invalid!!', item
                else:
                    print 'Fail', item
        else:
            print 'Bad', raw
        return tasklist

    def process_body(self, raw, task):
        if type(raw) == dict:
            expanded = 'notes' in raw or 'items' in raw
            if expanded:
                if 'notes' in raw:
                    task['notes'] = raw['notes']
                if 'items' in raw:
                    task['items'] = self.process_subtasks(raw['items'])
                return True
        task['items'] = self.process_subtasks(raw)

    def prepare_yaml(self):
        '''Return a simplified list of tasks [with dates converted to strings]'''
        return [tasktoyaml(sub) for sub in self.tasks]

def tasktoyaml(task):
    task = task.copy()
    task['created'] = task['created'].strftime(time_fmt)
    task['modified'] = task['modified'].strftime(time_fmt)
    if task['completed']:
        task['completed'] = task['completed'].strftime(time_fmt)
    else:
        task['completed'] = ''
    task['items'] = [tasktoyaml(sub) for sub in task['items']]
    main = collapse_string(task)
    if task['notes']:
        res = {main:{'notes': block(task['notes'])}}
        if task['items']:
            res[main]['items'] = task['items']
    elif task['items']:
        res = {main:task['items']}
    else:
        res = main
    return res

# vim: et sw=4 sts=4
