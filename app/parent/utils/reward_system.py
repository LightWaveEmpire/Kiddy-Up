from parent.models import Child, Parent, Task, Earned_Reward
from parent.utils import table_access
import sys

'''
Call this to mark a task as *Pending* for a child.

:param c_object: the child that owns the task
:param t_object: the task object to be completed
'''
def complete_task(c_object, t_object):
    c = c_object
    t = t_object

    #mark the task as pending 
    t.status = "PEND"
    t.save()

def purchase_reward(c_object, r_object):
    c = c_object
    r = r_object
    targetPoints = r.cost
    currentPoints = c.current_points
    print(f'\n\nDEBUG: Active Child = {c}\n\n', file=sys.stderr)
    print(f'\n\nDEBUG: Target Reward = {r}\n\n', file=sys.stderr)
    if currentPoints >= targetPoints:
        c.current_points = currentPoints - targetPoints
        c.save()
        earned_reward = Earned_Reward(child=c, reward=r)
        earned_reward.save()

    '''
    Not sure how this is done with Foreign Key
    earnedRewards = Earned_Reward()
    '''

def parent_validate_task(t_object):
    t = t_object
    t.status = "COMP"
    t.save()

    c = t.child_set.all().get()
    old_points = c.current_points
    c.current_points = old_points + t.point_value
    c.save()

def parent_invalidate_task(t_object):
    t = t_object
    t.status = "OPEN"
    t.save()
