#!/usr/bin/env python

import os
from os.path import join

def memoize(fn):
    cache = {}
    def meta(*a):
        if a not in cache:
            cache[a] = fn(*a)
        return cache[a]
    return meta

@memoize
def parse_gitconfig(gcfile):
    values = {}
    section = ''
    with open(gcfile) as f:
        for line in f:
            if line.startswith('['):
                section = line.strip()[1:-1]
            elif '=' in line:
                k, v = line.split('=', 1)
                values[section + '.' + k.strip()] = v.strip()
    return values

@memoize
def git_config(cwd, userdir):
    cgit = join(cwd, '.git', 'config')
    ugit = join(userdir, '.gitconfig')
    config = {}
    if os.path.isfile(ugit):
        config.update(parse_gitconfig(ugit))
    if os.path.isfile(cgit):
        config.update(parse_gitconfig(cgit))
    return config

# vim: et sw=4 sts=4
