'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/

'''

import os
import sys
from os.path import join

import logging
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
    '''Run the 'init' command!'''

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
    pass

# vim: et sw=4 sts=4
