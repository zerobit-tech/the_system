from django.contrib.sites.models import Site


def get_external_url():
    current_site = Site.objects.get_current()
    return f"{current_site.domain}"


def get_external_url_for_object(object):
    return f"{get_external_url()}{object.get_absolute_url()}"

def get_external_url_with_string(remaining_url):
    return f"{get_external_url()}{remaining_url}"