import shlex
import sys
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload

__commands = [ 
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -n loc_default",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q useractivity -n loc_default",

"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction -n process_transaction",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_01 -n process_transaction_01",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_02 -n process_transaction_02",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_03 -n process_transaction_03",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_04 -n process_transaction_04",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_05 -n process_transaction_05",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_06 -n process_transaction_06",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_07 -n process_transaction_07",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_08 -n process_transaction_08",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_09 -n process_transaction_09",
"celery -A SMSCenter worker --without-gossip --without-mingle --without-heartbeat --loglevel=debug -Ofair --pool=solo -Q process_transaction_10 -n process_transaction_10",


"rm -f 'celerybeat.pid'",
# https://github.com/celery/django-celery-beat
"celery -A SMSCenter beat --loglevel=debug --scheduler django_celery_beat.schedulers:DatabaseScheduler",
"celery -A SMSCenter worker --loglevel=debug --without-gossip --without-mingle --without-heartbeat -B -n loc_beat_2",
]


def restart_celery():
    cmd = 'pkill -f "celery worker"'
    if sys.platform == 'win32':
        cmd = 'taskkill /f /t /im celery.exe'

    subprocess.call(shlex.split(cmd))
    for command in  __commands:
        subprocess.Popen(shlex.split(command))


class Command(BaseCommand):

    def handle(self, *args, **options):
        restart_celery()
        #autoreload.run_with_reloader(restart_celery)
