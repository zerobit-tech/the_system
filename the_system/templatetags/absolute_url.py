from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.simple_tag()
def absolute_url(instance):
    return_string = str(instance)
    try:
        abs_url = instance.get_absolute_url()
        return_string = f"<a href='{abs_url}'> {instance} </a>"
    except:
        return_string = str(instance)

    return mark_safe(return_string)
    