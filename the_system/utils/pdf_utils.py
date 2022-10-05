
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import select_template
from django.utils import translation

from xhtml2pdf import pisa
import logging
logger = logging.getLogger('ilogger')



def render_to_pdf_old(template_src, context_dict={}, language=None):
    translated = False
    if language:
        current_language = translation.get_language()
        try:
            translation.activate(language)
            template = select_template(template_src)
            html  = template.render(context_dict)
            result = BytesIO()
            translated = True
        except Exception as e:
            translated = False
        finally:
            translation.activate(current_language)              

    if not translated:
        template = select_template(template_src)
        html  = template.render(context_dict)
        result = BytesIO()
    
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def render_to_pdf(template_src, context_dict={}, language=None):

    pdf, result = template_to_pdf(template_src,context_dict,language)
    return HttpResponse(result.getvalue(), content_type='application/pdf')


def template_to_pdf(template_src, context_dict={}, language=None):

    templates = []
    if isinstance(template_src, (list, tuple)):
        templates = template_src
    else:
        templates.append(template_src)



    translated = False
    if language:
        current_language = translation.get_language()
        try:
            translation.activate(language)
            template = select_template(templates)
            html  = template.render(context_dict)
            result = BytesIO()
            translated = True
        except Exception as e:
            translated = False
        finally:
            translation.activate(current_language)              

    if not translated:
        template = select_template(templates)
        html  = template.render(context_dict)
        result = BytesIO()
    
    
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)

    print(">>>> pdf.err ", pdf.err )
    return (pdf,result) if not pdf.err else (None,None)