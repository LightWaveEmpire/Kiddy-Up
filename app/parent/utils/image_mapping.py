# import os
# from array import *
# from parent.models import Task, Child, Parent

def get_task_image(task_description : str) -> str:
    """
    Returns some reference for an image based on the task description

    param: task_description: from the task details, will be used to identify the task image

    :return: a reference to an image to use for the child view

    """

    # step 0: if condition for child level.
    	# if file.startswith(condition):
    # step 1: read in task_description
    # step 2: split task_description into individual words
    # step 3: search filename for each word
    # step 4: return filename if words match

    # task_description = task.description
    # curr_user = task.child
    # comp_level = curr_user.comp_level
    # newlist = []

    # newlist.append(task_description.split())

    # for root, dirs, files in os.walk(r'static/task_images/'):
    #     for file in files:
    #         if file.startswith(str(comp_level)):
    #             if all(x in newlist for x in file):
    #                 return file
    #             else:
    #                 return "static/task_images/default_task_image.jpg"

    return "task_images/default_task_image.jpg"
