from parent.models import Child, Task, Original_Task

'''
Creates Original_Task entries from a list if they do not already exist

:param p_object: parent that owns the tasks
:param listOfEvents: list of strings that will be turned into otasks
'''
def create_otasks_from_list(p_object, listOfEvents)
    for item in listOfEvents
        if not Original_Task.objects.filter(otask=item).exists()
            t = Original_Task(parent=p_object, otask=item)
            t.save()

'''
Create child tasks from Original_Task table if they do not already exist
'''
def create_child_tasks_from_otask()
    for ot in Original_Task.objects.all()
        if not ot.has_created_task()
            ot.turn_into_child_task()
