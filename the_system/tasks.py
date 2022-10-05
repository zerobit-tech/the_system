from __future__ import absolute_import, unicode_literals
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from SMSCenter import celery_app 
import celery
import logging
from the_system.utils.date_time_utils import _write_fake_time

logger = logging.getLogger('ilogger')
class MyTask(celery.Task):
 def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('{0!r} failed: {1!r}'.format(task_id, exc))

@celery_app.task(name="sum_two_numbers")
def add(x, y):
    logger.debug("calling add")
    return x + y



@celery_app.task(name="next_day")
def next_day():
    now = timezone.localtime(timezone.localtime(timezone.now())) + timezone.timedelta(days=1)
    _write_fake_time(now)

@celery_app.task(name="next_hour")
def next_hour():
    now = timezone.localtime(timezone.localtime(timezone.now())) + timezone.timedelta(hours=1)
    _write_fake_time(now)
