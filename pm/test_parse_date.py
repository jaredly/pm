#!/usr/bin/env python

import pytest
import datetime
import parse_date

@pytest.mark.parametrize(('input', 'expected'), (
    ('04:12', {'hour': 4, 'minute': 12}),
    ('4:12',  {'hour': 4, 'minute': 12}),
    ('4:2',   {'hour': 4, 'minute':  2}),
    ('4:02',  {'hour': 4, 'minute':  2}),
    ('', False),
    ('4', False),
    ('08', False),
    (':02', False),
    ('2:', False),
    ('2-3', False)
))
def test_parse_time(input, expected):
    '''@tests parse_time.parse_date'''
    if expected is False:
        assert parse_date.parse_time(input) == False
    else:
        assert parse_date.parse_time(input) == expected

@pytest.mark.parametrize(('input', 'expected'), (
    ('8', {'day': 8}),
    ('8-7', {'month': 8, 'day': 7}),
    ('8-7-06', {'month': 8, 'day': 7, 'year': 2006}),
    ('', False),
    ('a', False),
    ('8:9', False),
    ('8-a', False),
    ('8-7-6', False)
))
def test_parse_date(input, expected):
    '''@tests parse_time.parse_time'''
    if expected is False:
        assert parse_date.parse_date(input) == False
    else:
        assert parse_date.parse_date(input) == expected

deftime = {
    'year':2013, 'month': 5, 'day': 4, 'hour': 3, 'minute': 2
}

today = datetime.datetime(year=2000, month=1, day=20, hour=13, minute=55)
dtime = datetime.datetime(**deftime)
tomorrow = today + datetime.timedelta(1)
yesterday = today - datetime.timedelta(1)

@pytest.mark.parametrize(('input', 'expected'), (
    ('today', today),
    ('TodAy', today),
    ('tomorrow', tomorrow),
    ('yesterday', yesterday),
    ('04-10-13', {'month': 4, 'day': 10, 'year': 2013}),
    ('04-10-13.4:30', {'month': 4, 'day': 10, 'year': 2013, 'hour': 4, 'minute': 30}),
    ('', dtime),
    ('toda', False),
    ('tomorra', False),
))
def test_parse_datetime(input, expected):
    if expected is False:
        with pytest.raises(ValueError):
            res = parse_date.parse_datetime(input, dtime, today)
    else:
        result = parse_date.parse_datetime(input, dtime, today)
        if isinstance(expected, datetime.datetime):
            assert result == expected
        elif isinstance(expected, dict):
            dct = deftime.copy()
            dct.update(expected)
            assert result == datetime.datetime(**dct)

# vim: et sw=4 sts=4
