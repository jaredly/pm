#!/usr/bin/env python

import pytest
import parse_tasks
import datetime

import yaml
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
    ('fly||today', {'name':'fly', 'created': 'today'}),
    ('fly|||tomorrow', {'name':'fly', 'modified': 'tomorrow'}),
    ('fly||||yesterday', {'name':'fly', 'completed': 'yesterday'}),
    ('fly||||10:20', {'name':'fly', 'completed': '10:20'}),
))
def test_expand_string(input, output):
    if output is False:
        with pytest.raises(ValueError):
            res = parse_tasks.expand_string(input, today)
    else:
        task = parse_tasks.inflate_task(output, today)
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
    task = parse_tasks.inflate_task({}, today)
    task2 = parse_tasks.inflate_task(json.loads(output.strip()), today)
    ydata = yaml.load(input)
    tmap = parse_tasks.TaskMap([], today)
    tmap.process_body(ydata, task)
    compare_tasks(task, task2)

text2 = '''
- one
# [{"name": "one", "id": 1}] #
- one|1
- two
# [{"name": "one", "id": 1}, {"name": "two", "id": 2}] #
- one|2
- two
# [{"name": "one", "id": 2}, {"name": "two", "id": 3}] #
- one|1
- two
- three|2
# [{"name": "one", "id": 1},
   {"name": "two", "id": 3},
   {"name": "three", "id": 2}] #
- one|1:
    - two
# [{"name": "one", "id": 1, "items": [{"name": "two", "id": 2}]}] #
- one:
    - two|1
# [{"name": "one", "id": 2, "items": [{"name": "two", "id": 1}]}] #
'''
inputs2 = [one.strip().split('\n#') for one in text2.split('#\n') if one.strip()]
@pytest.mark.parametrize(('input', 'output'), inputs2)
def test_parse_tasks(input, output):
    ydata = yaml.load(input)
    tmap = parse_tasks.TaskMap(ydata, today)
    tasks = [parse_tasks.inflate_task(item, today) for item in json.loads(output.strip())]
    [compare_tasks(t1, t2, True) for t1, t2 in zip(tmap.tasks, tasks)]

def compare_tasks(t1, t2, check_id=False):
    for k in t1:
        if k == 'id' and not check_id:
            continue
        elif k == 'items':
            [compare_tasks(s1, s2, check_id) for s1, s2 in zip(t1['items'], t2['items'])]
        else:
            assert t1[k] == t2[k]

text3 = '''
- one
+++
- one|1|05-04-13.03:02|05-04-13.03:02|
===
- one:
  - two
+++
- one|1|05-04-13.03:02|05-04-13.03:02|:
  - two|2|05-04-13.03:02|05-04-13.03:02|
'''
inputs3 = [one.strip().split('\n+++\n') for one in text3.split('\n===\n') if one.strip()]
@pytest.mark.parametrize(('input', 'output'), inputs3)
@pytest.mark.now
def test_parse_unparse(input, output):
    ydata = yaml.load(input)
    tmap = parse_tasks.TaskMap(ydata, today)
    rawd = tmap.prepare_yaml()
    res  = yaml.dump(rawd, default_flow_style=False)
    assert output.strip() == res.strip()

    # parse the generated output, make sure it matches
    tmap2 = parse_tasks.TaskMap(yaml.load(res), today)
    assert tmap.tasks == tmap2.tasks

# vim: et sw=4 sts=4
