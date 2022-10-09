import sys
from django.shortcuts import render
 
 
from django.http import Http404
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from the_user.decorators import otp_required,must_be
from the_user.initial_groups import TECH_SUPPORT,CUSTOMER_CARE_REP

from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from django.conf import settings
from the_system.utils.date_time_utils import _write_fake_time
from django.core.cache import cache
import logging
logger = logging.getLogger('ilogger')

from the_system.health_check import check_health


@login_required
@otp_required
@must_be(group_name=CUSTOMER_CARE_REP)
def health(request):
    context = {'health_data_list': check_health(request)}
    return render(request, 'the_system/health_check.html',context)


# -------------------------------------------------------
#
# -------------------------------------------------------
@login_required
@otp_required
@must_be(group_name=TECH_SUPPORT)
def invalidate_cache(request):
    cache.clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


 

# def add_days(request,days):
#     import os
#     now = timezone.localtime(timezone.now()) + timezone.timedelta(days=days)
#     date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
#     logger.debug("timezone.localtime(timezone.now())" , timezone.localtime(timezone.now()),date_time_str)

#     os.environ["FAKETIME"] = date_time_str  #  string must be "YYYY-MM-DD hh:mm:ss" or "+15d"
#     return JsonResponse({"newdate": timezone.localtime(timezone.now()),"newdate2": datetime.today()})

# -------------------------------------------------------
#
# -------------------------------------------------------
@login_required
@otp_required
def add_time(request):
    if not settings.DEBUG:
        raise Http404


    import os
    from sys import platform
    import time


        
        
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
        cache.clear()
    return render(request, 'the_system/add_time.html', {})



        