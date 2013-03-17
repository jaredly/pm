'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/
'''

from pm import cli

import argparse
import pytest

def pytest_funcarg__parser(request):
    return argparse.ArgumentParser()

def parses(parser, args, values):
    res = parser.parse_args(args)
    for k, v in values.items():
        assert k in res and getattr(res, k) == v

def test_argdict_normal(parser):
    '''You can add a normal argument'''
    cli.add_argdict(parser, {'dest': 'man'})
    parses(parser, ['fun'], {'man':'fun'})
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_argdict_option(parser):
    '''You can add an option'''
    cli.add_argdict(parser, {'options':['-m', '--man'], 'dest':'man'})
    parses(parser, ['-m', 'sad'], {'man':'sad'})
    parser.parse_args([])

def test_argdict_option_required(parser):
    '''You can add an option'''
    cli.add_argdict(parser, {'options':['-m', '--man'], 'dest':'man', 'required':True})
    parses(parser, ['-m', 'sad'], {'man':'sad'})
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_argdict_exclude(parser):
    '''You can add a mutually exclusive pair'''
    cli.add_argdict(parser, {'exclude':[
        {'options':['--foo'], 'dest':'foo', 'default':True},
        {'options':['--bar'], 'dest':'bar', 'default':True}
    ]})
    parses(parser, ['--foo', 'what'], {'foo':'what'})
    parses(parser, ['--bar', 'what'], {'bar':'what'})
    with pytest.raises(SystemExit):
        parser.parse_args(['--foo', 'what', '--bar', 'other'])
    parser.parse_args([])

def test_argdict_exclude_required(parser):
    '''You can add a mutually exclusive pair'''
    cli.add_argdict(parser, {'exclude':[
        {'options':['--foo'], 'dest':'foo', 'default':True},
        {'options':['--bar'], 'dest':'bar', 'default':True}
    ], 'required': True})
    parses(parser, ['--foo', 'what'], {'foo':'what'})
    parses(parser, ['--bar', 'what'], {'bar':'what'})
    with pytest.raises(SystemExit):
        parser.parse_args(['--foo', 'what', '--bar', 'other'])
    with pytest.raises(SystemExit):
        parser.parse_args([])

def test_argdict_baddict(parser):
    '''You need one of those three signatures'''
    with pytest.raises(ValueError):
        cli.add_argdict(parser, {'foo':'bar'})

# vim: et sw=4 sts=4
