from .models import SystemConfig
from django.contrib import admin

from django.conf import settings
from the_system.settings import _get_setting

 

def SystemConfigContextProcessor(request):

    debug  = False
    if settings.DEBUG:
        debug = True

    app_name = _get_setting('APP_NAME','APP NAME') # SystemConfig.get("APP_NAME")
    powered_by = _get_setting('POWERED_BY','MAGIC') #SystemConfig.get("POWERED_BY")
    setup_admin()
 
    return {"app_name": app_name,"powered_by":powered_by,"in_debug":debug}


def setup_admin():
 

    admin.site.site_header = _get_setting('ADMIN_SITE_HEADER',_get_setting('APP_NAME','APP NAME'))
    admin.site.site_title = _get_setting('ADMIN_SITE_TITLE',_get_setting('APP_NAME','APP NAME'))
    admin.site.index_title = _get_setting('ADMIN_INDEX_TITLE',_get_setting('APP_NAME','APP NAME'))