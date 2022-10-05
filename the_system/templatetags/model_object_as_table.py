from dataclasses import Field
from django import template
register = template.Library()
from django.db.models.fields.reverse_related import ForeignObjectRel,ManyToOneRel,OneToOneRel,ManyToManyRel
from django.db.models.fields import CharField
@register.inclusion_tag("the_system/model_object_as_table.html") # ,takes_context=True
def model_object_as_table(instance):
    """
    Returns verbose_name for a field.
    """

    field_data =[]
    try:
        fields =  instance._meta.get_fields()
    except:
        fields = None

    if fields:
        for field in fields:
            try:
                label =  field.verbose_name.title()
            except:
                label = field.name
            
            value = get_value(instance,field)
            field_data.append({"label":label, "value":value})


            print("========================================================START")
            print(field, isinstance(field,ManyToOneRel) , value is None)
            print("========================================================END")

    
    return {"field_list":field_data}

def get_value(instance,field):

    if isinstance(field,ManyToOneRel) or isinstance(field,OneToOneRel) or isinstance(field,ManyToManyRel) or isinstance(field,ForeignObjectRel):
       
        try:
            return getattr(instance, field.name).get_absolute_url() #field_name 
        except Exception as e:
            return str(e)

    if field.choices:
        selected_value = [c for c in field.choices if c[0]==getattr(instance, field.name)][0]
        return f"{selected_value[0]}:{selected_value[1]}"
    return  getattr(instance, field.name)