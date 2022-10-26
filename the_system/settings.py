from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
 
from django.conf import settings

class AppSettings():
    SITES_ENABLED = "django.contrib.sites" in settings.INSTALLED_APPS
    SOCIALACCOUNT_ENABLED = "allauth.socialaccount" in settings.INSTALLED_APPS

    LOGIN_REDIRECT_URL = getattr(settings, "LOGIN_REDIRECT_URL", "/")

    USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

app_settings = AppSettings()

def _get_setting(key, default):
    return_value =  getattr(settings, key, default)
    if return_value is None:
        return_value = default
    return return_value
    

 


def get_page_size():
    page_size = 25
    try:
        page_size = _get_setting('PAGE_SIZE',25)
    except AttributeError:
        page_size = 0
    except(TypeError, ValueError):
        page_size = 0


    if page_size <= 0:
        page_size = 25

    return page_size


 