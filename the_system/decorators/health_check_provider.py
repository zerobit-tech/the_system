
from functools import wraps

_registered_health_check_providers = {}

 

  

def health_check_provider(check_point_name):
    def health_check_decorator(func):
        """
        function must accept 1 input parameter => request
        and return a tuple of healty(true/false) and string message or list of string messages
        """
        global _registered_health_check_providers


        _registered_health_check_providers[str(check_point_name).capitalize()] = func
        @wraps(func)
        def actual_decorator(*args, **kwargs):
            value = func(*args, **kwargs)
            return value

        return actual_decorator
    
    return health_check_decorator