
from functools import wraps

registered_health_check_providers = []

def health_check(func):
    """
     function must accept 1 input parameter => request
     and return a tuple of healty(true/false) and string message
    """


    global registered_health_check_providers
    if func not in registered_health_check_providers:
        registered_health_check_providers.append(func)

    @wraps(func)
    def actual_decorator(*args, **kwargs):
        value = func(*args, **kwargs)
        return value

    return actual_decorator