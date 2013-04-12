'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/
'''

import os
import sys
import datetime
from os.path import join

import syck
from parse_tasks import TaskMap

def tail(f, window=20):
    BUFSIZ = 1024
    f.seek(0, 2)
    bytes = f.tell()
    size = window
    block = -1
    data = []
    while size > 0 and bytes > 0:
        if (bytes - BUFSIZ > 0):
            # Seek back one whole BUFSIZ
            f.seek(block*BUFSIZ, 2)
            # read BUFFER
            data.append(f.read(BUFSIZ))
        else:
            # file too small, start from begining
            f.seek(0,0)
            # only read what was not read
            data.append(f.read(bytes))
        linesFound = data[-1].count('\n')
        size -= linesFound
        bytes -= BUFSIZ
        block -= 1
    return ''.join(data).splitlines()

def last_lines(fn):
    return tail(open(fn), 2)

class UserError(Exception):
    '''The user did something wrong'''

class ProjectManager:
    consts = {
        'DIR_NAME': '.pm',
        'PROJECT_FILE': 'project.yaml',
        'TASKS_FILE': 'tasks.yaml',
        'TIMESHEET_FILE': 'timesheet.yaml',
        'CONFIG_FILE': 'config.yaml',
        'PROJECT_TEMPLATE': '''\
name: {name}
author: {author}
version: {version}
items:
'''
    }

    def __init__(self, basedir):
        self.basedir = basedir
        self.files = {}
        self.files['TASKS_FILE'] = join(self.basedir, self.consts['DIR_NAME'],
                                          self.consts['TASKS_FILE'])

    def init(self, name, author, version):
        pm = join(self.basedir, self.consts['DIR_NAME'])
        if os.path.isdir(pm):
            raise UserError('{} already exists!'.format(self.consts['DIR_NAME']))
        try:
            os.mkdir(pm)
        except:
            raise UserError('Invalid project directory: {}'.format(basedir))
        text = self.consts['PROJECT_TEMPLATE'].format(name=name, author=author, version=version)
        open(join(pm, self.consts['PROJECT_FILE']), 'w').write(text)
        open(join(pm, self.consts['TIMESHEET_FILE']), 'w').write('')
        open(join(pm, self.consts['CONFIG_FILE']), 'w').write('')

    def start(self, what):
        pm = join(self.basedir, self.consts['DIR_NAME'])
        fn = join(pm, self.consts['TIMESHEET_FILE'])
        lines = last_lines(fn)
        if lines:
            last = lines[-1].strip()
            if last.startswith('-') or last.startswith('start'):
                raise UserError('Already working on {}'.format(lines[0]))
        open(fn, 'aw').write('- name: {}\n  start: {}\n  '.format(what,
                                datetime.datetime.now().isoformat()))

    def stop(self, done=False):
        pm = join(self.basedir, self.consts['DIR_NAME'])
        fn = join(pm, self.consts['TIMESHEET_FILE'])
        lines = last_lines(fn)
        if not lines:
            print lines, pm, fn
            raise UserError('Not working on anything')
        last = lines[-2].strip()
        if not (last.startswith('-') or last.startswith('start')):
            print lines, pm, fn
            raise UserError('Not working on anything')
        text = 'end: {}\n'.format(datetime.datetime.now().isoformat())
        if done:
            text += '  done: true\n'
        open(fn, 'aw').write(text)

    def next(self, what, done=False):
        self.stop(done)
        self.start(what)

    def update(self, date=None):
        '''Update eveything ...

        if date is given, treat that as "today"
        '''

        if date is None:
            date = datetime.datetime.now()

        # load the main project file

        # load the tasks
        data = open(self.files['TASKS_FILE']).read()
        yaml = syck.load(data)
        tmap = TaskMap(yaml, date)
        out  = syck.dump(tmap.prepare_yaml())[3:].strip()
        open(self.files['TASKS_FILE']+'.new.yaml', 'w').write(out + '\n')

        # load the goals

        # load the timesheet



    

# vim: et sw=4 sts=4
