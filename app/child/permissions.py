from .apps import ChildConfig

def is_in_group_child(user):
    return user.groups.filter(name=ChildConfig.name).exists()
