
from contextlib import contextmanager
import time
from hashlib import md5
from django.core.cache import cache
from django.utils import timezone
import logging
logger = logging.getLogger('ilogger')

 
# ----------------------------------------------------------
#
# ----------------------------------------------------------
@contextmanager
def memcache_lock(lock_id, oid,lock_duration=60*5):
    timeout_at = time.monotonic() + lock_duration  
    # cache.add fails if the key already exists
    status = cache.add(lock_id, oid, lock_duration)
 
    try:
        yield status
    finally:
  
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if time.monotonic() > timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)

# ----------------------------------------------------------
#
# ----------------------------------------------------------
def _get_object_key(object, extra_id=""):
    tran_id_hexdigest = md5(str(object).encode('utf-8')).hexdigest()
    lock_id = f"start-{str(object)}-lock-{tran_id_hexdigest}-{extra_id}-end".replace(' ','_')
    return lock_id
# ----------------------------------------------------------
#
# ----------------------------------------------------------
def lock_object(object, extra_id="", lock_duration=60*5):
    """
        lock_duration=60*5 Lock expires in 5 minutes
    """
    lock_id = _get_object_key(object, extra_id=extra_id)
    print("lock_id", lock_id)
    with memcache_lock(lock_id, str(timezone.now()) , lock_duration=lock_duration ) as acquired:
        if acquired:
            return True
        else:
            return False
# ----------------------------------------------------------
#
# ----------------------------------------------------------
def release_object_lock(object,extra_id=""):
    lock_id = _get_object_key(object, extra_id=extra_id)
    cache.delete(lock_id)