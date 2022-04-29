import sys
from django.shortcuts import render
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth.decorators import login_required
 
from django.utils import timezone
from datetime import datetime
 
from django.http import JsonResponse
from django.conf import settings
from .utils import _write_fake_time

import logging
logger = logging.getLogger('loc_logger')



class ToggleTheme(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format = None):
        theme = request.data["theme"]
        if theme:
            request.session["uitheme"] = theme

        return Response({"done": True}, status=status.HTTP_200_OK)


# def add_days(request,days):
#     import os
#     now = timezone.localtime(timezone.now()) + timezone.timedelta(days=days)
#     date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
#     logger.debug("timezone.localtime(timezone.now())" , timezone.localtime(timezone.now()),date_time_str)

#     os.environ["FAKETIME"] = date_time_str  #  string must be "YYYY-MM-DD hh:mm:ss" or "+15d"
#     return JsonResponse({"newdate": timezone.localtime(timezone.now()),"newdate2": datetime.today()})



def add_time(request):
    import os
    from sys import platform
    import time

    if not settings.DEBUG:
        raise Http404
        
        
    days = int(request.GET.get('d',0)) if request.GET.get('d') else 0
    minutes = int(request.GET.get('m',0)) if request.GET.get('m') else 0
    seconds = int(request.GET.get('s',0)) if request.GET.get('s') else 0
    hours = int(request.GET.get('h',0)) if request.GET.get('h') else 0



    now = timezone.localtime(timezone.localtime(timezone.now())) + timezone.timedelta(minutes=minutes,seconds=seconds,hours=hours)

    print("------------------------- Testing time zone --------------------")
    print("now", now, "<:>",now.utcoffset())
    print("astimezone", now.astimezone())

    _write_fake_time(now.astimezone())

    #logger.debug("timezone.localtime(timezone.now())" , timezone.localtime(timezone.now()),date_time_str)

    # os.environ["FAKETIME"] = date_time_str  #  string must be "YYYY-MM-DD hh:mm:ss" or "+15d"

    for i in range(1,days+1):
        now = now + timezone.timedelta(days=1)
        _write_fake_time(now.astimezone())
        time.sleep(5)
    return render(request, 'the_system/add_time.html', {})



        