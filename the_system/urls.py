from django.urls import re_path, path
from . import views
 


app_name = 'the_system'
urlpatterns = [

  
    
   # path("adddays/<int:days>",views.add_days,name="add_days"),
    path("addtime",views.add_time,name="add_time"),
    path("invalidatecache",views.invalidate_cache,name="invalidate_cache"),
    # re_path(r'^totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
    # re_path(r'^totp/login/(?P<token>[0-9]{6})/$', views.TOTPVerifyView.as_view(), name='totp-login'),
 
]


 