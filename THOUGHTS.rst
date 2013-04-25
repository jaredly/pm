
-------------
General Notes
-------------

  timesheet
'''''''''''''

- this week (xx-xx-xxxx)
  - today (xx-xx-xxxx):
    - id: xx              goal ID
      start: xx:xx        start time
      end: xx:xx          end time
      done: bool          wether I reached the goal
      comment:            anything extra you want to say
    - xx xx:xx-xx:xx +
  - yesterday (xx-xx-xxxx):
- last week (xx-xx-xxxx)
  ...
- (xx-xx-xxx)
  ...

If there's no note, show condensed form

CMD:

- start
  -c add a comment

- stop
  -c add a comment
  [group]
    -s skip the next task and start the one following
    -n go on to the next

  default behavior is don't start another one.

- done
  -c add a comment
  [group]
    -s skip the next task and start the one following
    -n go on to the next

  default behavior is don't start another one.

- update

  Checks named days and weeks, updates accordingly. Also checks weeks against
  config.week_starts_on.

  goal setting
''''''''''''''''

  looks like: [goal id]|[task id]

- daily goals:
  - tomorrow (xx-xx-xxxx)
    ...
  - today (xx-xx-xxxx)
    - id: xx      goal ID
      task:       task ID
      --optional--
      type:       [done] | start | # hours
      note:       anything you want to say

    -- if there's no note, use a condensed form --

    - xx|xx       type: done
    - xx|xx -     type: start
    - xx|xx -yy   type: yy hours
  - yesterday (xx-xx-xxxx)
    ...
  - (xx-xx-xxxx)
- weekly goals:
  - next week (xx-xx-xxxx)
    ...
  - this week (xx-xx-xxxx)
    ...
  - last week (xx-xx-xxxx)
    ...
  - (xx-xx-xxxx)

Goals in a day or week *are ordered*.

- update
  -d --date xx-xx-xxxx OR [today], yesterday
  
    this changes what pm thinks is the "current" date when updating things.

  Goes through the goals.ymal, finding undated entries. Essentially if it
  finds a (today|yesterday|tomorrow|this week|next week|last week) without a
  date attached, it fills in the blanks with today==[--date].

  It also goes through and renames entries appropriately. 

CONFIG: week_starts_on : monday | sunday

  If, while running update, pm finds a week whose date doesn't start on the
  config.week_starts_on parameter, it asks "weeks found that start on the
  wrong day. Should I go through and fix them?"

  planning
''''''''''''

- name: Task Name
  created: xx-xx-xxxx
  -- optional --
  priority: A B C [blank]
  completed: false
  description: >
    A block of text
  items:
    - ...
    - ...

  -- if there's only a name and created (+ completed) use condensed form --

- my name
- xx name
- +done task
- xx +done task

