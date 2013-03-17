#!/usr/bin/env python

import os
import sys
from os.path import join
import argparse
from pm import ProjectManager, UserError

def create_argparser(name, options={}, arguments=[], sub_commands={}):
    '''Create an argument parser from the options, arguments, and
    sub_commands'''
    base = argparse.ArgumentParser(**options)
    for arg in arguments:
        add_argdict(base, arg)
    if sub_commands:
        group = base.add_subparsers()
        for name, arguments in sub_commands.items():
            parser = group.add_parser(name)
            parser.set_defaults(cmd_name=name)
            for arg in arguments:
                add_argdict(parser, arg)
    return base

def add_argdict(parser, arg):
    '''Add an argument to a parser according to a dictionary.
    
    WARNING: Does not test for recursion in exclude groups.'''
    if 'exclude' in arg:
        items = arg['exclude']
        del arg['exclude']
        group = parser.add_mutually_exclusive_group(**arg)
        for sub in items:
            add_argdict(group, sub)
    elif 'options' in arg:
        options = arg['options']
        del arg['options']
        parser.add_argument(*options, **arg)
    elif 'dest' in arg:
        dest = arg['dest']
        del arg['dest']
        parser.add_argument(dest, **arg)
    else:
        raise ValueError('Invalid options specified {}'.format(arg))

def get_option(options, prompt='Which? '):
    '''Get a one of many choice from the user'''
    inp = None
    while inp is None or not (0 <= inp < len(options)):
        for i, option in options:
            print '{}. {}'.format(i+1, option)
        try:
            res = raw_input(prompt)
        except EOFError:
            return None
        except KeyboardInterrupt:
            return None
        try:
            inp = int(res) - 1
        except:
            pass
    return options[inp]

def get_yesno(prompt, default='y'):
    '''Get a yes/no question answered'''
    inp = None
    while inp is None or inp[0] not in 'yn':
        try:
            res = raw_input(prompt + '[{}] '.format(default))
        except (EOFError, KeyboardInterrupt):
            return None
        if not res:
            return default == 'y'
        res = res.lower()
    return res[0] == 'y'

def get_string(prompt, default=None, blank=True):
    '''Get a custom string, with an optional default, and a flag for allowing
    blank values'''
    inp = None
    if default:
        prompt += '[{}] '.format(default)
        try:
            res = raw_input(prompt)
        except (EOFError, KeyboardInterrupt):
            return None
        if not res:
            res = default
        return res
    elif blank:
        try:
            res = raw_input(prompt)
        except (EOFError, KeyboardInterrupt):
            return None
        return res
    while not inp:
        try:
            inp = raw_input(prompt)
        except (EOFError, KeyboardInterrupt):
            return None
    return inp

def find_basedir(curdir):
    '''Find a directory with a ".git" folder in it'''
    ocd = None
    while curdir != '/' and ocd != curdir:
        ocd = curdir
        if os.path.isdir(join(curdir, '.git')):
            return curdir
        curdir = os.path.dirname(curdir)

def run_init(options):
    '''Run the 'init' command!'''

    basedir = find_basedir(os.getcwd())
    if not basedir:
        raise UserError('No git repository found')
    if os.path.isdir(join(basedir, ProjectManager.consts['DIR_NAME'])):
        raise UserError('{}/ already exists. exiting.'.format(ProjectManager.consts['DIR_NAME']))
    project = get_string('Project Name: ', os.path.basename(basedir))
    if not project:
        sys.stderr.write('\nCanceled\n')
        return
    author = get_string('Your Name: ', blank=False)
    if not author:
        sys.stderr.write('\nCanceled\n')
        return
    version = get_string('Version Number: ', '0.1')
    if not version:
        sys.stderr.write('\nCanceled\n')
        return
    pm = ProjectManager(basedir)
    pm.init(project, author, version)

NAME = 'Project Manager'
COMMANDS = {
    'init': [{
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
    }],
}

commands = {
    'init': run_init
}

def run_cmd(args):
    '''Run the whole thing!'''
    parser = create_argparser(NAME, sub_commands=COMMANDS)
    res = parser.parse_args(args)
    if 'cmd_name' in res and res.cmd_name in commands:
        try:
            commands[res.cmd_name](res)
        except UserError as e:
            sys.stderr.write('Error: {}\n'.format(e))
            return
    else:
        sys.stderr.write('Invalid command specified.')
        return

# vim: et sw=4 sts=4
