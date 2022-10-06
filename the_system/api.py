 
from django.urls import reverse_lazy
from ninja import Router 
from ninja.security import django_auth
from ninja import Schema , Field


from the_user.api_auth import BearerAuth
from the_system.decorators.health_providers import registered_health_check_providers


router = Router()
 
 

# -------------------------------------------------------
#
# -------------------------------------------------------
@router.get("/health", url_name="system_health",auth=[django_auth,BearerAuth()])
def health(request):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    #permission_classes = [permissions.IsAuthenticated,IsClient]

    content = {'healthy': True,'message':""}
    for checker in registered_health_check_providers:
        healthy = True
        message = ""
        try:
            healthy,message = checker(request)
        except Exception as e:
            healthy = False        
            message = str(e)

        if not healthy:
            content["healthy"] = False
            content["message"] = str(message)
            break

   
    return content


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

    users_url = reverse_lazy("api:toggle_theme")

    return 200, {"done": True,"users_url":str(users_url)}