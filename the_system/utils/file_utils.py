import string
import traceback
import logging
from django.template.loader import render_to_string, select_template

logger = logging.getLogger('ilogger')


def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.
 
Note: this method may produce invalid filenames such as ``, `.` or `..`
When I use this method I prepend a date string like '2009_01_15_19_46_32_'
and append a file extension like '.txt', so I avoid the potential of using
an invalid filename.
 
"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.strip().replace(' ','_') # I don't like spaces in filenames.
    return filename



def get_template_name(template_name):
    templates_to_check = []
    if isinstance(template_name, (list, tuple)):
        templates_to_check = template_name
    else:
        templates_to_check.append(template_name)

    try:
        template = select_template(templates_to_check)
        return template.template.name
    except Exception as e:
        logger.error(f"@admin: Error processing template : {e} :{traceback.format_exc()}")
        raise e