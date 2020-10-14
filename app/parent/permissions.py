from .apps import ParentConfig

def is_in_group_parent(user):
    return user.groups.filter(name=ParentConfig.name).exists()
