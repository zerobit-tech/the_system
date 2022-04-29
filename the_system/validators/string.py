from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

 

def non_blank(value):
    if not str(value).strip():
        raise ValidationError(
            _('%(value)s cannot be empty'),
            params={'value': value},
        )