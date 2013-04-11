#!/usr/bin/env python

import pytest
import parse_tasks
import datetime

import syck
import json

deftime = {
    'year':2013, 'month': 5, 'day': 4, 'hour': 3, 'minute': 2
}
today = datetime.datetime(**deftime)
tomorrow = today + datetime.timedelta(1)
yesterday = today - datetime.timedelta(1)

def mktime(dct):
    t = deftime.copy()
    t.update(dct)
    return datetime.datetime(**t)

@pytest.mark.parametrize(('input', 'output'), (
    ('Hello world', {'name':'Hello world'}),
    ('Do homework|5', {'name': 'Do homework', 'id': 5}),
    ('fly||today', {'name':'fly', 'created': today}),
    ('fly|||tomorrow', {'name':'fly', 'modified': tomorrow}),
    ('fly||||yesterday', {'name':'fly', 'completed': yesterday}),
    ('fly||||10:20', {'name':'fly', 'completed': mktime({'hour':10, 'minute':20})}),
))
def test_expand_string(input, output):
    if output is False:
        with pytest.raises(ValueError):
            res = parse_tasks.expand_string(input, today)
    else:
        task = parse_tasks.new_task(output)
        result = parse_tasks.expand_string(input, today)
        assert result == task

text = '''
notes: doit
# {"notes": "doit"} #
items:
    - fan
# {"items": [{"name": "fan"}]} #
- fan
# {"items": [{"name": "fan"}]} #
- one
- two
# {"items": [{"name": "one"}, {"name": "two"}]} #
- one:
    notes: things
# {"items": [{"name": "one", "notes": "things"}]} #
- one:
    - two
# {"items": [{"name": "one", "items": [{"name": "two"}]}]} #
one:
    - two
# {"items": [{"name": "one", "items": [{"name": "two"}]}]} #
one:
    - two
    - three
# {"items": [{"name": "one", "items": [{"name": "two"}, {"name": "three"}]}]} #
one:
    notes: two
three:
    notes: four
# {"items": [{"name": "one", "notes": "two"},
             {"name": "three", "notes": "four"}]} #
'''
inputs = [one.strip().split('\n#') for one in text.split('#\n') if one.strip()]
@pytest.mark.parametrize(('input', 'output'), inputs)
def test_process_body(input, output):
    task = parse_tasks.new_task()
    task2 = parse_tasks.inflate_task(json.loads(output.strip()))
    yaml = syck.load(input)
    tmap = parse_tasks.TaskMap([], today)
    tmap.process_body(yaml, task)
    # parse_tasks.process_body(yaml, task, today)
    compare_tasks(task, task2)
    # assert task == task2

def compare_tasks(t1, t2):
    for k in t1:
        if k == 'id':
            continue
        elif k == 'items':
            [compare_tasks(s1, s2) for s1, s2 in zip(t1['items'], t2['items'])]
        else:
            assert t1[k] == t2[k]

# vim: et sw=4 sts=4