# ------------------------------------------------------------
#  {self.app_name.lower()}/views.py 
# ------------------------------------------------------------

import logging

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView,CreateView, CreateView
from django.views.decorators.debug import sensitive_variables,sensitive_post_parameters
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator

from the_system.utils.request_utils import get_client_ip,get_request_meta
from the_user.mixin import OPTRequiredMixin,CCRRequiredMixin

from {self.app_name.lower()}.models import {self.model_name}
from {self.app_name.lower()}.forms import {self.model_name}CreateForm

logger = logging.getLogger('ilogger')

# ------------------------------------------------------------
#
# ------------------------------------------------------------
class {self.model_name}CreateView(OPTRequiredMixin,SuccessMessageMixin,CreateView):

    template_name_suffix = "{self.template_suffix}"
    model = {self.model_name}
    form_class = {self.model_name}CreateForm
    success_message = ""# _("Card %(nick_name)s created successfully")


    # ------------------------------------------------------------
    def get_context_data(self, **kwargs):
        # add mode data in context for template to use 
        data = super().get_context_data(**kwargs)
        # user = self.request.user
        # data['account'] = self.get_account()
        return data




    # ------------------------------------------------------------
    def get_object(self,queryset=None):
        id =  self.kwargs['{self.id_field}']
        obj = get_object_or_404({self.model_name},{self.id_field}=id)
        return obj 

    # ------------------------------------------------------------
    def get_form_kwargs(self):
        # Return the keyword arguments for instantiating the form.
        # The get_form_kwargs method will return a dictionary with the kwargs that will be passed to the __init__ of your form.
        
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    # ------------------------------------------------------------
    def get_initial(self):
        # Returns the initial data for the forms to use.
      
        initial = super().get_initial()
        # self.account = self.get_account()
        # initial['account'] =self.account
        return  initial


 

    # ------------------------------------------------------------
    def form_valid(self, form):
        # If the form is valid, save the associated model. 
        clean = form.cleaned_data
    
        response = super().form_valid(form)
        
        # meta = {{}}
        # request = self.request
        # meta["user_ip"] =  get_client_ip(request)
        # meta["HTTP_USER_AGENT"] = get_request_meta(request,'HTTP_USER_AGENT')
        # meta["HTTP_REFERER"] = get_request_meta(request,'HTTP_REFERER')
        # save meta

        return response

    # ------------------------------------------------------------
    #@method_decorator(sensitive_post_parameters('card_number','cvv'))
    #@method_decorator(sensitive_variables('card_number','cvv'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)