from django.core.exceptions import ObjectDoesNotExist
from parent.models import Child, Parent

'''
Gets a child object that matches the parent and string name.

:param pobject: parent object of the child
:param string_name: name of the child that is being searched
'''
def get_child(pobject, string_name):
    try:
        c = Child.objects.get(parent=pobject, name=string_name)
    except ObjectDoesNotExist:
        return None
    
    return c
