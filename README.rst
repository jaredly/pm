
***************
Project Manager
***************

Can I get a more generic title?
-------------------------------

But then we have a nice two letter script name! ``pm``.

Commands:
---------

pm init
  Initialize the project. This will find the root project directory and create
  a ``.pm/`` directory next to it. ATM I'm just targeting git, but I don't
  know that it will be really hard to extend it to mercurial, etc.

pm plan
  This prints a list of ... tasks/bugs that you might want to work on, and
  asks you which one you really want to work on. So you type in a comma
  separated list. Order is important, as it indicates generally in what order
  you want to work on things.

  Ways things can be sorted

  - most recently created
  - highest ranked
  - oldest
  
  With numbers next to them. And you type like 17,4,2,12

pm edit
  This opens up the project definition file, which is a YAML file. You can
  edit it, and then when you exit the editor it will validate everything and
  update the webserver (if it's running).

pm serve
  Start a web server! It's an awesome web app. You can create, arrange, and
  organize your project to your heart's content.

  [1.1] You can also use the time tracking from the web server. Like toggle.

pm config
  Open the config file in your default editor. Which is also a YAML file

pm start
  Start working! It will ask you what task you want to be working on

pm resume
  Start again where you left off. This checks to see the "stopped" id in the
  config file. Or maybe the history file?

pm pause
  pause the timer. optional message why.

pm stop
  Stop the timer and save as "stopped" in the config file the current task id

pm done
  You've completed whatever it was you are working on! Default behavior is to
  commit and possibly also run the test suite?

  It also asks you what you want to work on next. If you have a plan already,
  it shows you the tasks you said you wanted to work on (perhaps only the
  first 10 or so) and asks which one you want to work on [default is the next
  one, -1 or Ctrl-D for quit].

  param -s will also "stop" meaning you won't be prompted for the next one.

  -e or typing e when prompted takes you to edit the project file first.
  
pm stask
  create a subtast and start working on it

Models
------

An item or task of sub-thing can have a number of attributes:

name
  right. If the name starts with "+", that means it's done. If pm looks at
  your project file and sees an item marked done with out a "completed"
  attribute, it fills it in with the current time.
id
  the number associated with the task. When PM looks at your file and it finds
  something without an id, it gives it one.
items
  the list of sub-items
due
  when this needs to be done by. optional
completed
  the date when it was completed.
tags:
  comma separated list of tags (can be used for versioning, etc.)

If an item only has a name and id and nothing else, it is represented just as the
scalar name, not as a dictionary. So it would be "## name". where ## is an
integer.

project.yaml
------------

The project file ``project.yaml`` looks like::

    name: Project Manager
    id: 1
    author: Jared
    items:
      - name: Website
        id: 2
        items:
          - name: style
            id: 3
          - name: content
            id: 4
      - name: Project
        items:
          - name: command-line
          - name: server

bugs.yaml
---------

This is where we record all of the bugs you made. :) and fix.

A bug's attributes:

id
  number
test
  if this is ``~``, then we look for a test with the name of test_bug_## with
  ## being the id num of the bug.
created
  datetime
closed
  datetime # this should be auto assigned by pm, when you say "done", the test
  should pass.
status
  unconfirmed | confirmed | worksforme
  
config.yaml
-----------

The file ``config.yaml`` contains configuration options. Things like:

- auto go to the next item after saying "done"
- ??? other things
- idk
- !! have the option of dotted id numbers (like dad does); so 1.10.3 for a
  sub-sub-item, instead of a single integer.
- allow_untested_bugs ; otherwise pm won't let you close a bug that doesn't
  have a test attached to it (without you passing a --untestable parameter or
  something)

timesheet.yaml
------------

Here we have recorded all the times you work on things. This looks like::

  - id: idnum you were working on
    start: datetime started
    end: datetime ended
    finished: whether or not you finished what you were working on

Thoughts:

  - what about directory-awareness? Like if you're in the /static/ directory,
    that means something? Like it only shows you some subset of the
    bugs/project items/...? I don't know if that would be best.
  - connect functions to tests. so on the diff, look at new functions created
    and new tests created ... and connect them? Put comments in the test, ~and
    in the function? maybe mostly/just in the test

