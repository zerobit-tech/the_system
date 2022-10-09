 
from django.urls import reverse_lazy
from ninja import Router 
from ninja.security import django_auth
from ninja import Schema , Field


from the_user.api_auth import BearerAuth
from the_system.health_check import check_health


router = Router()
 
 
class HealthData(Schema):
    healthy: bool
    message: str
    checkpoint: str
# -------------------------------------------------------
#
# -------------------------------------------------------
@router.get("/health", url_name="system_health",auth= BearerAuth(), response= HealthData)
def health(request):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    #permission_classes = [permissions.IsAuthenticated,IsClient]

    content = {'healthy': True,'message':"All good","checkpoint":""}

    health_data_list = check_health(request)
    for health_data in health_data_list:
        check_point = health_data['checkpoint']
        healthy = health_data['healthy']
        message = health_data['message']

        if not healthy:
            content = {'healthy': healthy,'message':message,"checkpoint":check_point}

    return 200, content


# -------------------------------------------------------
#
# -------------------------------------------------------

class ThemeSchema(Schema):
    theme:str 

@router.post("/toggletheme", url_name="toggle_theme",auth=django_auth)
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