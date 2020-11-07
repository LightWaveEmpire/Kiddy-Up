... # other imports here


# all functions that are not model specific can go in app/parent/utils/*.py
# I put some stubs in there but not all
from .utils import image_mapping, entity_extraction, reward_system, calendar_pull



... # other classes here


class Task(models.Model):

    ... # other assigments/definitions here

    def create_from_otask(parent: Parent, otask: Original_Task) -> bool:
        """
        Creates new tasks from the original task imported from the external source

        :param parent: The parent that owns the original task and the children the new tasks will be assigned to
        :param otask: The original task to be transformed into new child tasks

        :return: null
        """

        added_tasks = False

        tasks = get_list_of_tasks(otask) # This will be a function that processes an original task and returns a list of "task" dictionaries to be created

        if tasks:
            added_tasks = True # tasks will be added below
            # May be multiple child tasks from one otask (one for each child)
            for task in tasks:
                t = Task(original_task = otask, parent = parent, child = task.child, name = task.name, description = task.description, status, image = task.task_image, date = task.date, location = task.location)
                t.save()

        return added_tasks






class Original_Task(models.Model):

    ... # other assigments/definitions here

    def get_list_of_tasks(self: Original_Task) -> list:
        """
        Returns list of dict items with task details from an original task

        :return: list of dict items with task details from an original task
        """
        task_list = []
        # Get the parent instance that the original_task instance is linked to
        parent = Parent.objects.get(user_id=self.parent__user_id)
        raw_task = self.otask
        # extract_entities() will take in a raw string and return a dict file with the following keys, values (values in text):
        # task['name'] = name
        # task['description'] = description
        # task['people'] = people (a list of names)
        # task['date'] = date
        # task['location'] = location
        task_details = entity_extraction.extract_entities(otask)
        # iterate through the list of identified people and make a new task for each child involved
        for person in task_details['people']
            try:
                # Only get children that belong to the parent
                child = Child.objects.get(name=person, parent = parent)

                # Will this be an image or a file location? Django handles images well and can probably do this well
                task_image = image_mapping.get_task_image(task_details['description'])

                # child dict from spaCy extract
                child_task = {}
                child_task['name'] = task_details['name']
                child_task['description'] = task_details['description']
                child['child'] = child
                child_task['date'] = task_details['date']
                child_task['location'] = task_details['location']
                child_task['image'] = task_image
                task_list.append(child_task)
                break
            except:
                print (f'Child {person} does not belong to {parent.name}: Task will not be added for {person}')

        return task_list

