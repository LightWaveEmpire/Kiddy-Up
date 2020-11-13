from django.core.exceptions import ObjectDoesNotExist
from parent.models import Child, Parent


#get child function by searching with string
def get_child(pobject, string_name)
    try:
        c = Child.objects.get(parent=pobject, name=string_name)
    except ObjectDoesNotExist:
        return None
    
    return c
