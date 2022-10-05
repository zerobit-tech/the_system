# ------------------------------------------------------------
#  {self.app_name.lower()}/views.py 
# ------------------------------------------------------------

import logging
from django.views.generic.edit import DeleteView
from django.http import Http404

from the_user.mixin import OPTRequiredMixin,CCRRequiredMixin,CCMRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from the_user.utils import user_is
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER
from the_clients.models import Client

from {self.app_name.lower()}.models import {self.model_name}
from {self.app_name.lower()}.forms import {self.model_name}UpdateForm

logger = logging.getLogger('ilogger')

class {self.model_name}DeleteView(CCMRequiredMixin,SuccessMessageMixin, DeleteView):
    model = {self.model_name} 
    success_message = 'Deleted successfully.'
    template_name_suffix = "{self.template_suffix}"


    def get_success_url(self):
        return {self.model_name}.get_on_delete_url()

    # ------------------------------------------------------------
    def get_object(self,queryset=None):
        user = self.request.user
        id =  self.kwargs['{self.id_field}']


        if user_is(user,CUSTOMER_CARE_REP):
            obj = get_object_or_404({self.model_name},{self.id_field}=id)

        # elif Client.is_client(user):
        #     obj = get_object_or_404(self.model_name},{self.id_field}=id,created_by=user.client)
            
        # else:
        #     obj = get_object_or_404(self.model_name},{self.id_field}=id, customer__user=user)
        
        if obj is None:
            raise Http404
            
        return obj  