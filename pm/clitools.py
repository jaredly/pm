'''
This is part of Project Manager, (c) 2013 Jared Forsyth. This has been
released under the GPLv3 license.

http://jabapyth.github.com/pm/

'''

def get_option(options, prompt='Which? '):
    '''Get a one of many choice from the user'''
    inp = None
    while inp is None or not (0 <= inp < len(options)):
        for i, option in options:
            print '{}. {}'.format(i+1, option)
        try:
            res = raw_input(prompt)
        except EOFError:
            return None
        except KeyboardInterrupt:
            return None
        try:
            inp = int(res) - 1
        except:
            pass
    return options[inp]

def get_yesno(prompt, default='y'):
    '''Get a yes/no question answered'''
    inp = None
    while inp is None or inp[0] not in 'yn':
        try:
            res = raw_input(prompt + '[{}] '.format(default))
        except (EOFError, KeyboardInterrupt):
            return None
        if not res:
            return default == 'y'
        res = res.lower()
    return res[0] == 'y'

def get_string(prompt, default=None, blank=True):
    '''Get a custom string, with an optional default, and a flag for allowing
    blank values'''
    inp = None
    if default:
        prompt += '[{}] '.format(default)
        try:
            res = raw_input(prompt)
        except (EOFError, KeyboardInterrupt):
            return None
        if not res:
            res = default
        return res
    elif blank:
        try:
            res = raw_input(prompt)
        except (EOFError, KeyboardInterrupt):
            return None
        return res
    while not inp:
        try:
            inp = raw_input(prompt)
        except (EOFError, KeyboardInterrupt):
            return None
    return inp

# vim: et sw=4 sts=4
