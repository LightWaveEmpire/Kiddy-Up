from parent.models import Child, Task, Original_Task

#create child tasks from original_tasks
def create_child_tasks_from_otask()
    for ot in Original_Task.objects.all()
        if not ot.has_created_task()
            ot.turn_into_child_task()
