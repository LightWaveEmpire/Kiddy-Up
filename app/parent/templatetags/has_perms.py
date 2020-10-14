from django import template
from parent.permissions import is_in_group_parent
register = template.Library()

@register.filter
def has_perms(user):
    return is_in_group_parent(user)
