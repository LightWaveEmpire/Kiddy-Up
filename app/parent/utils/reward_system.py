from parent.models import Child, Parent, Task
from parent.utils import table_access

'''
Call this to mark a task as completed for a child.

:param c_object: the child that owns the task
:param t_object: the task object to be completed
'''
def complete_task(c_object, t_object):
    #give points to the child
    c = c_object
    t = t_object
    old_points = c.current_points
    new_points = t.point_value
    
    c.current_points = old_points + new_points
    c.save()
 
    #mark the task as completed
    t.status = "COMP"
    t.save()
