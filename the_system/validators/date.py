from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

 # Use Python's built-in datetime module

from django.utils import timezone

def must_be_18(value):
    age_today = age(value)
    if age_today < 18 :
        raise ValidationError(
            _('Must be 18 years or old. (it %(value)s as of today)'),
            params={'value': age_today},
        )



def age(birthdate):
    # Get today's date object
    # today = timezone.localtime(timezone.localtime(timezone.now()))
    today =  timezone.localtime(timezone.now()) 
    
    # A bool that represents if today's day/month precedes the birth day/month
    one_or_zero = ((today.month, today.day) < (birthdate.month, birthdate.day))
    
    # Calculate the difference in years from the date object's components
    year_difference = today.year - birthdate.year
    
    # The difference in years is not enough. 
    # To get it right, subtract 1 or 0 based on if today precedes the 
    # birthdate's month/day.
    
    # To do this, subtract the 'one_or_zero' boolean 
    # from 'year_difference'. (This converts
    # True to 1 and False to 0 under the hood.)
    age = year_difference - one_or_zero
    
    return age