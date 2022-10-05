from django import template
from django.conf import settings
import json
from the_system.money import ZERO_DOLLAR
# this is required
register = template.Library()
from django.utils.translation import gettext as _

 


@register.filter(name='fill_dots')
def fill_dots(value, length):
    # lenght_to_apply = length -len(str(value))
   
    return   f"{_(str(value)).ljust(length, '.')}:  ".replace("..",'. ')

 