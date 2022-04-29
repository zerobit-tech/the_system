from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .settings import get_page_size
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.datetime_safe import time
from datetime import date,time,datetime

from django.utils.text import slugify
import random
import string


import logging
logger = logging.getLogger('loc_logger')

def get_paginator(request, object_list):

    paginator = Paginator(object_list, get_page_size())  # 3 post per page

    page_number = request.GET.get('page')

    try:
        paginator_object = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        paginator_object = paginator.page(1)
    except EmptyPage:
        page_number = paginator.num_pages
        paginator_object = paginator.page(paginator.num_pages)

    return page_number, paginator_object




def make_timezone_aware(date):
    return timezone.make_aware(timezone.datetime.combine(parse_date(str(date)), time.min))

def move_to_eod(date_to_convert):
    cutoff_time = datetime.strptime("23:59:59","%H:%M:%S")
    return change_time(date_to_convert,cutoff_time)


def move_to_sod(date_to_convert):
    cutoff_time = datetime.strptime("00:00:00","%H:%M:%S")
    return change_time(date_to_convert,cutoff_time)

def get_start_of_year():
    return timezone.localtime(timezone.now()).replace(month=1,day=1,hour=0,minute=0,second=0)

def change_time(date_to_convert, time):
    if isinstance(date_to_convert, date) and not isinstance(date_to_convert, datetime) :

        date_to_convert = make_timezone_aware(date_to_convert)

    final_date = timezone.localtime(date_to_convert).replace(hour=0, minute=0, second=0)
    final_date = final_date+timezone.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
    return final_date


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_request_meta(request,key):
    return request.META.get(key.upper(),'')





def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def _write_fake_time(time_now):
    import os
    from sys import platform
    date_time_str = time_now.strftime("%Y-%m-%d %H:%M:%S")


    if platform == "linux" or platform == "linux2":

        file_data= ""
        with open('/etc/faketimerc', "w") as myfile:
            myfile.write(date_time_str)
            #
        with open('/etc/faketimerc', "r") as myfile:
            file_data = myfile.read()