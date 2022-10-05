from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

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


 