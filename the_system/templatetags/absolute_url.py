from django import template
from django.utils.safestring import mark_safe
register = template.Library()
from django.utils.translation import gettext as _


@register.simple_tag()
def absolute_url(instance):
    return_string = str(instance)

    tooltip = None
    try: 
        tooltip = instance.get_tooltip()
    except:
        tooltip = None
    
    try:
        abs_url = instance.get_absolute_url()
        if tooltip:
            return_string = f"<a data-toggle='c-tooltip' data-placement='bottom'title='{_(tooltip)}' href='{abs_url}'> {instance} </a>"
        else:
            return_string = f"<a href='{abs_url}'> {instance} </a>"
    except:
        return_string = str(instance)

    return mark_safe(return_string)
    