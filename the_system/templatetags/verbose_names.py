from django import template
register = template.Library()

@register.filter(name='verbose_name')
def get_verbose_field_name(field_name,instance):
    """
    Returns verbose_name for a field.
    """
    try:
        return instance._meta.get_field(field_name).verbose_name.title()
    except:
        return f"{field_name}"