
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import select_template
from django.utils import translation
from django.template.loader import render_to_string, select_template

from xhtml2pdf import pisa
import logging
logger = logging.getLogger('ilogger')

# -------------------------------------------------
def template_to_string(language, template , context_data):
    return_string =""
    current_language = translation.get_language()
    try:  
        if language:
            translation.activate(language)
        
        return_string = render_to_string(template, context_data)
    
    except Exception as e:
        logger.error(f"@compilance: transalation failed: {template}")   
        return_string = render_to_string(template, context_data)
    finally:
        translation.activate(current_language)  

   
    
    return return_string
