from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.datetime_safe import time
from datetime import date,time,datetime

from django.utils.text import slugify
import random
import string


import logging
logger = logging.getLogger('ilogger')

 



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



def _write_fake_time(time_now):
    import os
    from sys import platform
    from pathlib import Path


    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    fake_time_file = os.path.join(BASE_DIR, 'faketimerc')
    fake_time_file_bkp = os.path.join(BASE_DIR, 'faketimerc_bkp')

    date_time_str = time_now.strftime('%Y-%m-%d %H:%M:%S')

    print(" date_time_str ", date_time_str , platform, fake_time_file)

    if platform == "linux" or platform == "linux2":

        file_data= ""
        try:

            with open(fake_time_file, "r") as myfile:
                file_data = myfile.read()
                print("file_data", file_data)

            os.environ['FAKETIME_TIMESTAMP_FILE'] = str(fake_time_file_bkp)

            with open(fake_time_file, "w") as myfile:
                myfile.write(date_time_str)
                
                
            os.environ['FAKETIME_TIMESTAMP_FILE'] =str(fake_time_file)

            with open(fake_time_file_bkp, "w") as myfile:
                myfile.write(date_time_str)
                

        except Exception as e:
            print("Error " , e)
