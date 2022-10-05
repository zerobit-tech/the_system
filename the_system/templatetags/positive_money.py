from django import template
from django.conf import settings
import json
from the_system.money import ZERO_DOLLAR
# this is required
register = template.Library()


 


@register.filter(name='positive_money')
def positive_money(amount):
    if amount<ZERO_DOLLAR:
        return ZERO_DOLLAR
    else:
        return amount 


@register.filter(name='blank_money')
def positive_money(amount):
    if amount== ZERO_DOLLAR:
        return "----"
    else:
        return amount 