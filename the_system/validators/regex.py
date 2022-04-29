from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
 
card_number_validator = RegexValidator(r'^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$', _('Invalid card number'))
cvv_validator = RegexValidator(r'^[0-9]{3,4}$', _('CVV must be 3 or 4 digit number'))
card_expiry_validator = RegexValidator(r'^(0[1-9]|1[0-2])([0-9]{2})$', _('Card expiry must be in MMYY format'))
usa_zip_validator = RegexValidator(r'^[0-9]{5}$', _('ZIP must be 5 digit number'))
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed."))

 

time_validator = RegexValidator(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$', _("Must be in HH:MM:SS format. Example 01:23:09"))