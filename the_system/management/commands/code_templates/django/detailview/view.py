# ------------------------------------------------------------
#  {self.app_name.lower()}/views.py 
# ------------------------------------------------------------

import logging
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, UpdateView
from django.utils.translation import gettext_lazy as _
from the_user.utils import user_is

from the_user.mixin import OPTRequiredMixin,CCRRequiredMixin
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER
from the_clients.models import Client

from {self.app_name.lower()}.models import {self.model_name}

logger = logging.getLogger('ilogger')

#----------------------------------------------------------------
#
#----------------------------------------------------------------
class {self.model_name}DetailsView(CCRRequiredMixin,SuccessMessageMixin, DetailView):
    model = {self.model_name}
  
    success_message = _('Info updated successfully.')
    def get_success_url(self):
        return self.get_object().get_absolute_url()

    # ------------------------------------------------------------
    def get_context_data(self, **kwargs):
        # Insert the single object into the context dict.
        context = {{}}
        {self.id_field} =  self.kwargs['{self.id_field}']
        # context['customer_info'] =  get_object_or_404(CustomerInfo,uuid=uuid)
        context.update(kwargs)

        return super().get_context_data(**context)

    # ------------------------------------------------------------
    def get_object(self,queryset=None):
        user = self.request.user
        id =  self.kwargs['{self.id_field}']


        if user_is(user,CUSTOMER_CARE_REP):
            obj = get_object_or_404({self.model_name},{self.id_field}=id)

        # elif Client.is_client(user):
        #     obj = get_object_or_404({self.model_name},{self.id_field}=id,created_by=user.client)
            
        # else:
        #     obj = get_object_or_404({self.model_name},{self.id_field}=id, customer__user=user)
        
        if obj is None:
            raise Http404

        return obj