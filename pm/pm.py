'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/
'''

import os
import sys
from os.path import join

class UserError(Exception):
    '''The user did something wrong'''

class ProjectManager:
    consts = {
        'DIR_NAME': '.pm',
        'PROJECT_FILE': 'project.yaml',
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
    

# vim: et sw=4 sts=4
