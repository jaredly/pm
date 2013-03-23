'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/
'''

import datetime

def lastmonday(day):
    return day - datetime.timedelta(day.weekday())

FMTS = ['%d', '%m-%d', '%m-%d-%Y']

def parse_num_week(text, today=None):
    '''Parse a week date from text
    
    If "today" is given, it fills in any information with that date'''

    day = parse_num_day(text, today)
    return lastmonday(day) if day else False

def parse_num_day(text, today=None):
    '''Parse a day from text
    
    If "today" is given, it fills in any information with that date'''

    if today is None:
        today = datetime.date.today()
    hyphens = text.count('-')
    if hyphens > 2:
        print 'toomanyhyphens'
        return False
    try:
        date = datetime.datetime.strptime(text, FMTS[hyphens]).date()
    except ValueError:
        print 'valueerror'
        return False
    if hyphens == 0:
        return today.replace(day=date.day)
    elif hyphens == 1:
        return today.replace(day=date.day, month=date.month)
    return date

def parse_week(text, default=None, today=None):
    '''Give a date that represents a week: a monday
    
    If "today" is given, it fills in any information with that date'''

    if today is None:
        today = datetime.date.today()
    this_week = lastmonday(today)
    if default is None:
        default = this_week
    text = text.lower()
    if text == 'this week' or text is None:
        return this_week
    if text == 'last week':
        return this_week - datetime.timedelta(days=7)
    if text == 'next week':
        return this_week + datetime.timedelta(days=7)
    result = parse_num_week(text)
    return result or default

def parse_day(text, default=None, today=None):
    '''Given mm-dd-yyyy or mm-dd or dd,
    or 'tomorrow' or 'yesterday' or 'today'

    If "today" is given, it fills in any information with that date'''

    if today is None:
        today = datetime.date.today()
    if default is None:
        default = today
    text = text.lower()
    if text is None or text == 'today':
        text = 'today'
    if text == 'yesterday':
        return today - datetime.timedelta(days=1)
    if text == 'tomorrow':
        return today + datetime.timedelta(days=1)
    result = parse_num_day(text)
    return result or default

# vim: et sw=4 sts=4
