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

from parse_date import parse_datetime

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
        'modified': None, 'completed': None, 'items': None}

def new_task(news={}):
    task = default_task.copy()
    task['items'] = []
    task.update(news)
    return task

def inflate_task(dct):
    task = new_task(dct)
    task['items'] = map(inflate_task, task['items'])
    return task

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
    return new_task(data)

class TaskMap:
    def __init__(self, raw, today):
        self.tmap = {}
        self.tasks = []
        self.unassigneds = {}
        self.unassigned = 0
        self.max = 0
        self.today = today
        self.tasks = self.process_subtasks(raw)

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
                if type(item) == dict:
                    if len(item) == 1:
                        k = item.keys()[0]
                        tasklist.append(self.add_task(k, item[k]))
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

def parse_tasks(fname):
    raw = syck.load(open(fname).read())
    tmap = TaskMap(raw)


# vim: et sw=4 sts=4
