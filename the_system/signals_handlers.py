 
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
import traceback 

from .signals import notify_user
import logging
logger = logging.getLogger('ilogger')
 
"""
notify.send(actor, recipient, verb, action_object, target, level, description, public, timestamp, **kwargs)


  example: justquick (actor) closed (verb) issue 2 (action_object) on activity-stream (target) 12 hours ago
"""

"""
def notify_user_handler(sender, recipient, verb, action_object=None, target=None, level='info', description="", public=True,  **kwargs):


"""
@receiver(notify_user)
def notify_user_handler(**kwargs):
    print("notify_usernotify_usernotify_usernotify_usernotify_usernotify_usernotify_user")
    try:
        kwargs.pop('signal', None)
        sender = kwargs.get('sender',None)
        if sender is None:
            sender= User.objects.get(username = 'SYSTEM')
            kwargs['sender'] = sender

        from notifications.signals import notify
        notify.send(**kwargs)
   
    except Exception as e:
        logger.error(f"{e}:{traceback.format_exc()}")
