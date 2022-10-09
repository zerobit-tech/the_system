
def check_health(request):
    """
    this function check and call all registerd health check providers

    health check provider takes one input --> request
                           return a tuple (bool,str|list)


    
    """

    from the_system.decorators.health_check_provider import _registered_health_check_providers

    health_data_list = []

    for check_point_name in _registered_health_check_providers:
        healthy = True
        messages = ""
        try:
            checker = _registered_health_check_providers[check_point_name]
            healthy,messages = checker(request)



        except Exception as e:
            healthy = False        
            messages = str(e)

        if not isinstance(messages, list):
            messages = [messages]

        health_data_list.append({"checkpoint":check_point_name , "healthy": healthy , "messages":messages})

    return health_data_list


