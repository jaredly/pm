'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/
'''

import yaml
from collections import OrderedDict

class quoted(str):
    '''Use ``quoted(val) if you want to override default scalar representation
    and have it quoted with ".'''

def quoted_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
yaml.add_representer(quoted, quoted_presenter)

class block(unicode):
    '''Use ``block(val)`` when you want the outputted YAML to be a folded
    block, instead of a normal flat scalar or quoted string (if it's long).'''

def block_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='>')
yaml.add_representer(block, block_presenter)

def ordered_dict_presenter(dumper, data):
    return dumper.represent_dict(data.items())
yaml.add_representer(OrderedDict, ordered_dict_presenter)

