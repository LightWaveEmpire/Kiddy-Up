from parent.models import Child, Task, Original_Task, Parent

'''
Creates Original_Task entries from a list if they do not already exist

:param p_object: parent that owns the tasks
:param listOfEvents: list of strings that will be turned into otasks
'''
def create_otasks_from_list(p_object, listOfEvents):
    for event, event_json in listOfEvents:
        if not Original_Task.objects.filter(otask=event, raw_otask=event_json, parent=p_object).exists():
            t = Original_Task(parent=p_object, otask= event, raw_otask=event_json)
            t.save()

'''
Create child tasks from Original_Task table if they do not already exist

:param p_object: parent that owns the tasks
'''
def create_child_tasks_from_otask(p_object):
    for ot in Original_Task.objects.filter(parent=p_object):
        if not ot.has_created_task():
            ot.turn_into_child_task()

'''
This function takes a string that will be stored as an Original_Task.

:param p_object: parent that will own the task
:param task_string: string to be stored into otask
'''
def create_otask_manually(p_object, task_string):
    ot = Original_Task(parent = p_object, otask = task_string)
    ot.save()
    ot.turn_into_child_task()
