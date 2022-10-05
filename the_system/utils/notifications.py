"""
notify.send(actor, recipient, verb, action_object, target, level, description, public, timestamp, **kwargs)


  example: justquick (actor) closed (verb) issue 2 (action_object) on activity-stream (target) 12 hours ago
"""

"""
def notify_user_handler(sender, recipient, verb, action_object=None, target=None, level='info', description="", public=True,  **kwargs):


"""
import logging
logger = logging.getLogger('ilogger')
 
def notify_user(**kwargs):
    print("notify_usernotify_usernotify_usernotify_usernotify_usernotify_usernotify_user")
    try:
        from notifications.signals import notify
        notify.send(**kwargs)
   
    except Exception as e:
        logger.error(e)
