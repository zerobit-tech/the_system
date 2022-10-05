# ------------------------------------------------------------
#  {self.app_name.lower()}/views.py 
# ------------------------------------------------------------

import logging
from django.shortcuts import render, redirect,get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from the_system.settings import get_page_size
from the_user.mixin import OPTRequiredMixin,CCRRequiredMixin,AdminRequiredMixin
from the_user.utils import user_is
from the_user.initial_groups import CUSTOMER_CARE_SUPERVISER, CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER
 

 
from {self.app_name.lower()}.models import {self.model_name}
from {self.app_name.lower()}.filters import {self.model_name}Filter

logger = logging.getLogger('ilogger')

# ------------------------------------------------------------
#
# ------------------------------------------------------------
class {self.model_name}List(ListView):
    model = {self.model_name}
    paginate_by = get_page_size()
    ordering = ['-pk']
    filterset_class = {self.model_name}Filter
    def get_queryset(self):
        user = self.request.user
       
        if user_is(user,CUSTOMER_CARE_REP):
            queryset = {self.model_name}.objects.all()
        else:
            queryset =  {self.model_name}.objects.filter(user=user).all()
 
        queryset = queryset.order_by("-pk")
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filterset'] = self.filterset

        return context 
