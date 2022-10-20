from django.contrib.sites.models import Site
from urllib.parse import urlsplit
from django.core.exceptions import  ImproperlyConfigured
from the_system.settings import app_settings, _get_setting


# ------------------------------------------------
#
# ------------------------------------------------
def get_external_url():
    current_site = Site.objects.get_current()
    return f"{current_site.domain}"


# ------------------------------------------------
#
# ------------------------------------------------

def get_external_url_for_object(object,request=None):
    return build_absolute_uri(request,object.get_absolute_url())


# ------------------------------------------------
#
# ------------------------------------------------
def get_external_url_with_string(remaining_url,request=None):
    return build_absolute_uri(request, location=remaining_url)


# ------------------------------------------------
#
# ------------------------------------------------
def build_absolute_uri(request, location, protocol=None):
    """request.build_absolute_uri() helper

    Like request.build_absolute_uri, but gracefully handling
    the case where request is None.
    """
 

    if request is None:
        if not app_settings.SITES_ENABLED:
            raise ImproperlyConfigured(
                "Passing `request=None` requires `sites` to be enabled."
            )
        from django.contrib.sites.models import Site

        site = Site.objects.get_current()
        bits = urlsplit(location)
        if not (bits.scheme and bits.netloc):
            uri = "{proto}://{domain}{url}".format(
                proto=_get_setting('DEFAULT_HTTP_PROTOCOL','https'),
                domain=site.domain,
                url=location,
            )
        else:
            uri = location
    else:
        uri = request.build_absolute_uri(location)
    # NOTE: We only force a protocol if we are instructed to do so
    # (via the `protocol` parameter, or, if the default is set to
    # HTTPS. The latter keeps compatibility with the debatable use
    # case of running your site under both HTTP and HTTPS, where one
    # would want to make sure HTTPS links end up in password reset
    # mails even while they were initiated on an HTTP password reset
    # form.
    if not protocol and _get_setting('DEFAULT_HTTP_PROTOCOL','https') == "https":
        protocol = _get_setting('DEFAULT_HTTP_PROTOCOL','https')
    # (end NOTE)
    if protocol:
        uri = protocol + ":" + uri.partition(":")[2]
    return uri