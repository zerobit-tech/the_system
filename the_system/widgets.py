from django import forms
import logging
logger = logging.getLogger('loc_logger')

class DateInput(forms.DateInput):
    input_type = 'date'