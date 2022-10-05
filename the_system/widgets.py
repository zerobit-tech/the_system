from django import forms
import logging
logger = logging.getLogger('ilogger')

class DateInput(forms.DateInput):
    input_type = 'date'