# ------------------------------------------------------------
#  {self.app_name.lower()}/filters.py 
# ------------------------------------------------------------

import logging

import django_filters
import django_filters as filters
from django_filters.views import FilterView

from django.utils.translation import gettext_lazy as _
from {self.app_name.lower()}.models import {self.model_name}

logger = logging.getLogger('ilogger')
# ------------------------------------------------------------
#
# ------------------------------------------------------------
class {self.model_name}Filter(django_filters.FilterSet):
    # start_date = filters.CharFilter(label='Article')
     class Meta:
        model = {self.model_name}
        fields = [{self.filter_fields}]
 