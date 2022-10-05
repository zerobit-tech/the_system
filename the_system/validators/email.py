from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from the_system.utils.email_utils import is_valid_email

def valid_email(value):
    is_valid, error_message = is_valid_email(value)
    if not is_valid:
        raise ValidationError(error_message)
  


 