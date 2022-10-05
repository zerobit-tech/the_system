# ------------------------------------------------------------
#  {self.app_name.lower()}/forms.py 
# ------------------------------------------------------------

import logging
from django import forms
from django.core.exceptions import ValidationError

from the_system.widgets import DateInput
from the_user.utils import user_is
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER
from django.utils.translation import gettext_lazy as _

from {self.app_name}.models import {self.model_name}

 
logger = logging.getLogger('ilogger')

# ------------------------------------------------------------
#
# ------------------------------------------------------------ 
class {self.model_name}UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request', None) # added by get_form_kwargs in view
        #self.account = kwargs.pop('account', None)
        
        super().__init__(*args, **kwargs)

        #self.fields['field_need_to_be_disabled'].disabled = True
        #self.fields['card'].queryset = self.account.cards.all()


    # ------------------------------------------------------------ 
    class Meta:
        model = {self.model_name}
        fields = [{self.form_fields}]
        #widgets = {{'hidden_field': forms.HiddenInput(),
        #            'date_field': DateInput(),
        #            'password_field':forms.PasswordInput()
        # }}
        
    # ------------------------------------------------------------ 
    {self.clean_field_methods}
    # ------------------------------------------------------------ 
    def clean(self):
        cleaned_data = super().clean()

        # if cleaned_data['field'] != 'valid':
        #     raise ValidationError(_('Invalid valide'), code='invalid')

 