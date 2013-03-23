'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/
'''

from pm import dates
from datetime import datetime, date, timedelta

last_monday = (
    (date(2000, 12, 18), date(2000, 12, 18)),
    (date(2000, 12, 17), date(2000, 12, 11)),
        )

def test_lm():
    '''Test the lastmonday(datetime.date) function'''

    for inp, out in last_monday:
        res = dates.lastmonday(inp)
        assert res == out, '{} : {} = {}'.format(inp, res, out)

def test_parse_num_day():
    '''test parse_num_day'''
    today = date(year=2013, day=22, month=3)
    data = (
        ('1', today.replace(day=1)),
        ('1-2', today.replace(day=2, month=1)),
        ('1-2-1000', date(year=1000, day=2, month=1)),
        ('x', False),
        ('1-1-1', False),
        ('1-x', False)
    )
    for inp, out in data:
        res = dates.parse_num_day(inp, today=today)
        assert res == out, '{} : {} = {}'.format(inp, res, out)

def test_parse_num_week():
    '''Test parse_num_week'''
    today = date(year=2013, day=22, month=3).replace(month=3, day=1)
    res = dates.parse_num_week('3-1', today=today)
    assert res == today - timedelta(today.weekday())

def test_parse_week():
    today = date(2013, day=22, month=3)
    this_week = dates.lastmonday(today)
    data = (
        ('this week', this_week),
        ('last week', this_week - timedelta(7)),
        ('next week', this_week + timedelta(7))
    )
    for inp, out in data:
        res = dates.parse_week(inp, today=today)
        assert res == out, '{} : {} = {}'.format(inp, res, out)

def test_parse_day():
    today = date(2013, day=22, month=3)
    data = (
        ('today', today),
        ('tomorrow', today + timedelta(1)),
        ('yesterday', today - timedelta(1))
    )
    for inp, out in data:
        res = dates.parse_day(inp, today=today)
        assert res == out, '{} : {} = {}'.format(inp, res, out)

# vim: et sw=4 sts=4
