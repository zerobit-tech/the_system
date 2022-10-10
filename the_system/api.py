 
from django.urls import reverse_lazy
from ninja import Router 
from ninja.security import django_auth
from ninja import Schema , Field

from typing import List
from the_user.api_auth import BearerAuth
from the_system.health_check import check_health
import logging
logger = logging.getLogger('ilogger')

router = Router(auth= BearerAuth())
internal_router = Router(auth=django_auth) 
 
# -------------------------------------------------------
#
# ------------------------------------------------------- 
class HealthData(Schema):
    checkpoint: str
    healthy: bool
    messages: list


class OverallHealthData(Schema):
    healthy: bool
    healthdata: List[HealthData]
# -------------------------------------------------------
#
# -------------------------------------------------------
@router.get("/health", url_name="system_health", response= OverallHealthData)
def health(request):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    #permission_classes = [permissions.IsAuthenticated,IsClient]

    overall_healthy = True

    health_data_dict = {'healthy': True,'messages':["All good"],"checkpoint":""}
    health_data_list= []

    # get all data
    for health_data in check_health(request):
        #check_point = health_data['checkpoint']
        healthy = health_data['healthy']
        #messages = health_data['messages']
        
        health_data_list.append(health_data)

        if not healthy:
            overall_healthy = False
 

    if not health_data_list:
        health_data_list.append(health_data_dict)

    return 200, {"healthy":overall_healthy,'healthdata': health_data_list}


# -------------------------------------------------------
#
# -------------------------------------------------------

class ThemeSchema(Schema):
    theme:str 

@internal_router.post("/toggletheme", url_name="toggle_theme")
def toggletheme(request, theme:ThemeSchema):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    #permission_classes = [permissions.IsAuthenticated,IsClient]

    new_theme = theme.dict().get("theme",None)
    if new_theme:
        request.session["uitheme"] = new_theme

    users_url = reverse_lazy("internalapi:toggle_theme")

    return 200, {"done": True,"users_url":str(users_url)}