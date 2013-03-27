'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/

'''

import os
import sys
from os.path import join

import logging
import datetime
from subprocess import call

from .clitools import get_option, get_yesno, get_string
from .commander import CommandManager
from .pm import ProjectManager, UserError
from .git import git_config

def find_basedir(curdir):
    '''Find a directory with a ".git" folder in it'''
    ocd = None
    while curdir != '/' and ocd != curdir:
        ocd = curdir
        if os.path.isdir(join(curdir, '.git')):
            return curdir
        curdir = os.path.dirname(curdir)

def ensure_basedir(curdir):
    basedir = find_basedir(curdir)
    if not basedir:
        raise UserError('No git repository found')
    if not os.path.isdir(join(basedir, ProjectManager.consts['DIR_NAME'])):
        raise UserError('no {}/ found. Need to run pm init?\n'
                        'exiting.'.format(ProjectManager.consts['DIR_NAME']))
    return basedir

cli = CommandManager('pm')

@cli.add([{
        'exclude': [
            {
                'options': ['-c', '--commit'],
                'dest': 'commit',
                'action': 'store_const',
                'const': True,
                'default': None,
                'help': 'Commit without prompting'
            },
            {
                'options': ['-n', '--no-commit'],
                'dest': 'commit',
                'action': 'store_const',
                'const': False,
                'default': None,
                'help': 'Don\'t commit'
            },
        ]
    }])
def init(options):
    '''Run the 'init' command!
    
    - default: create the stuff, then ask if you want to commit
    - -c commit without asking
    - -n don't commit, don't ask
    '''

    basedir = find_basedir(os.getcwd())
    if not basedir:
        raise UserError('No git repository found')
    if os.path.isdir(join(basedir, ProjectManager.consts['DIR_NAME'])):
        raise UserError('{}/ already exists. '
                        'exiting.'.format(ProjectManager.consts['DIR_NAME']))

    config = git_config(basedir, os.path.expanduser('~'))
    if 'user.name' in config and 'user.email' in config:
        username = config['user.name'] + ' <' + config['user.email'] + '>'
    else:
        username = None

    project = get_string('Project Name: ', os.path.basename(basedir))
    if not project:
        sys.stderr.write('\nCanceled\n')
        return
    author = get_string('Your Name: ', blank=False, default=username)
    if not author:
        sys.stderr.write('\nCanceled\n')
        return
    version = get_string('Version Number: ', '0.1')
    if not version:
        sys.stderr.write('\nCanceled\n')
        return
    pm = ProjectManager(basedir)
    pm.init(project, author, version)
    logging.info('[pm] initialized')
    if options.commit is not False:
        if options.commit or get_yesno('Git add and Commit? '
                                       '"Adding [pm] http://jabapyth.github.com/pm/"'):
            call(['git', 'add', '.pm', '-f'], cwd=basedir)
            call(['git', 'commit', '-m', 'Adding [pm] http://jabapyth.github.com/pm/'])

@cli.add([{
        'options': ['-d', '--date'],
        'dest': 'date',
        'default': None
    }])
def update(options):
    '''Update everything. Go through the yml files to see if anything needs updating.

    - -d --date xx-xx-xxxx | [today] | yesterday
    '''

    basedir = ensure_basedir(os.getcwd())
    pm = ProjectManager(basedir)
    pm.update(date)

@cli.add([{
    'dest': 'task'
}])
def start(options):
    '''Start things

    '''

    basedir = ensure_basedir(os.getcwd())
    pm = ProjectManager(basedir)
    pm.start(options.task)

@cli.add([])
def stop(options):
    '''Stop things'''
    basedir = ensure_basedir(os.getcwd())
    pm = ProjectManager(basedir)
    pm.stop()

@cli.add([])
def done(options):
    '''Done things'''
    basedir = ensure_basedir(os.getcwd())
    pm = ProjectManager(basedir)
    pm.stop(True)

@cli.add([{
    'dest': 'task'
}, {
    'options': ['-d', '--done'],
    'dest': 'done',
    'default': False,
    'action': 'store_true'
}])
def next(options):
    '''Done things'''
    basedir = ensure_basedir(os.getcwd())
    pm = ProjectManager(basedir)
    pm.next(options.task, options.done)


# vim: et sw=4 sts=4
