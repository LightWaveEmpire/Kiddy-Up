


def extract_entities(otask: str) -> dict:
    """
    Returns some reference for an image based on the task description

    param: task_description: from the task details, will be used to identify the task image

    :return: a reference to an image to use for the child view

    """
    default_task['name'] = "default task name"
    default_task['description'] = "default task description"
    default_task['people'] = ["default task person 1", "default task person 2"]
    default_task['date'] = "12/02/2021"
    default_task['location'] = "default task location"
    return default_task
