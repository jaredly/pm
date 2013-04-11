#!/usr/bin/env python

import datetime

time_fmt = '%m-%d-%y.%H:%M'

def parse_datetime(text, now):
    '''A full date looks like mm-dd-yy.HH:MM'''
    text = text.strip().lower()
    if not text:
        return None
    if text == 'today':
        return now
    if text == 'yesterday':
        return now - datetime.timedelta(days=1)
    if text == 'tomorrow':
        return now + datetime.timedelta(days=1)
    try:
        return datetime.datetime.strptime(text, time_fmt)
    except ValueError:
        pass
    # if it's not in the basic idea, then you get: 
    parts = text.split('.')
    dct = {'day': now.day, 'month': now.month, 'year': now.year,
           'minute': now.minute, 'hour': now.hour}
    if len(parts) == 2:
        date = parse_date(parts[0])
        if date is False:
            return None # raise ValueError('Invalid date: %s' % parts[0])
        dct.update(date)
        time = parse_time(parts[1])
        if time is False:
            return None # raise ValueError('Invalid time: %s' % parts[0])
        dct.update(time)
    elif len(parts) == 1:
        if '-' in text:
            date = parse_date(text)
            if date is False:
                return None # raise ValueError('Invalid date: %s' % parts[0])
            dct.update(date)
        elif ':' in text:
            time = parse_time(text)
            if time is False:
                return None # raise ValueError('Invalid time: %s' % parts[0])
            dct.update(time)
        else:
            return None # raise ValueError('Invalid date: %s' % text)
    else:
        return None # raise ValueError('Invalid date: %s' % text)
    return datetime.datetime(**dct)

def parse_date(text):
    '''Parse the date looks like MM-DD-YY, return False if it doesn't parse'''
    parts = text.split('-')
    try:
        parts = map(int, parts)
    except ValueError:
        return False
    if len(parts) == 1:
        return {'day': parts[0]}
    elif len(parts) == 2:
        return {'month': parts[0], 'day': parts[1]}
    elif len(parts) == 3:
        try:
            dt = datetime.datetime.strptime(text, '%m-%d-%y')
        except ValueError:
            return False
        return {'month': dt.month, 'day': dt.day, 'year': dt.year}
    return False

def parse_time(text):
    '''Parse the time in the format HH:MM'''
    parts = text.split(':')
    if len(parts) != 2:
        return False
    try:
        return dict(zip(('hour', 'minute'), map(int, parts)))
    except ValueError:
        return False

# vim: et sw=4 sts=4
