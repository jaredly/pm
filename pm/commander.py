'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/

'''

import argparse

class CommandManager:
    def __init__(self, name, options={}):
        self.name = name
        self.cmds = {}
        self.parser = argparse.ArgumentParser(**options)
        self.subgroup = False

    def add(self, options, name=None):
        '''Use as a @decorator, to add a command function'''
        def inner(cmd):
            _name = name if name else cmd.__name__
            if not self.subgroup:
                self.subgroup = self.parser.add_subparsers()
            self.addcmd(_name, options, cmd)
            return cmd
        return inner

    def addcmd(self, name, arguments, cmd):
        sub = self.subgroup.add_parser(name)
        self.cmds[name] = cmd
        for arg in arguments:
            add_argdict(sub, arg)

    def run(self, args):
        options = self.parser.parse_args(args)
        if 'cmd_name' in options and options.cmd_name in self.cmd:
            try:
                self.cmd[options.cmd_name](options)
            except UserError as e:
                sys.stderr.write('Error: {}\n'.format(e))
                return
        else:
            sys.stderr.write('Invalid command specified.')
            return

def add_argdict(parser, arg):
    '''Add an argument to a parser according to a dictionary.

    Examples:
        {
         'dest': 'thing',
         'options': ['-t', '--thing'],
         'action': 'store_true'
        },
        {
         'exclude': [arg_dict, ...]
        },
        {
         'dest': 'thing'
        }
    
    WARNING: Does not test for recursion in exclude groups.
    '''

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




# vim: et sw=4 sts=4
