import math
from decimal import *
from djmoney.money import Money
from the_system.money import ZERO_DOLLAR , USD
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

 

def greater_than_zero(value):
    if USD(value) <= ZERO_DOLLAR:
        raise ValidationError(
            _('Cannot be Zero)'),
        
        )