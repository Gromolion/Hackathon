from django import template
from ..models import *

register = template.Library()


@register.simple_tag(name='get_accesses')
def get_categories(folder_id, user_id):
    return Access.objects.filter(folder_id=folder_id, useraccess__user_id=user_id)