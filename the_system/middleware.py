from threading import local
from django.contrib.auth.models import User
import logging
logger = logging.getLogger('ilogger')

class TheSystemMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request.search_value = request.GET.get('search_value', "").strip()
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response


_user = local()

class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        
    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

def get_current_user():
    try:
        return _user.value
    except:
        return get_system_user()

def get_system_user():
    try :
        return User.objects.get(username="SYSTEM")
    except:
        return ""





# -----------------------------------------------------
# https://github.com/labd/django-session-timeout/blob/master/src/django_session_timeout/middleware.py
# -----------------------------------------------------
import time

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


SESSION_TIMEOUT_KEY = "_session_init_timestamp_"


class SessionTimeoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, "session") or request.session.is_empty():
            return

        init_time = request.session.setdefault(SESSION_TIMEOUT_KEY, time.time())

        expire_seconds = getattr(
            settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
        )

        session_is_expired = time.time() - init_time > expire_seconds

        if session_is_expired:
            request.session.flush()
            redirect_url = getattr(settings, "SESSION_TIMEOUT_REDIRECT", None)
            if redirect_url:
                return redirect(redirect_url)
            else:
                return redirect_to_login(next=request.path)

        expire_since_last_activity = getattr(
            settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY", False
        )
        grace_period = getattr(
            settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD", 1
        )

        if expire_since_last_activity and time.time() - init_time > grace_period:
            request.session[SESSION_TIMEOUT_KEY] = time.time()