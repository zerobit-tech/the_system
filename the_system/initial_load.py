from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .initial_groups import CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER, CUSTOMER_CARE_SUPERVISER, TECH_SUPPORT, ADMIN
import logging
logger = logging.getLogger('ilogger')

GROUPS = [CUSTOMER_CARE_REP, CUSTOMER_CARE_MANAGER, CUSTOMER_CARE_SUPERVISER, TECH_SUPPORT, ADMIN]

GROUP_PERMISSIONS = {
        CUSTOMER_CARE_REP : [('can open account', 'can_open_account'),
        ],  # list of tuple > name,code name


        CUSTOMER_CARE_MANAGER: [],
        CUSTOMER_CARE_SUPERVISER: [],
        TECH_SUPPORT: [],
        ADMIN: [],

}


def create_service_user():
        user,_ = User.objects.get_or_create(username = 'SYSTEM',
                                 first_name = "",
                                 last_name = "",
                                 email="system@example.com",
                                 password="Super@007",
                                 is_active = True
                                 )
        # user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

def create_initial_user_groups():
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            if created:
                pass



def create_initial_permissions():

    group_content_type = ContentType.objects.get(app_label='auth', model='group')

    for group_name in GROUP_PERMISSIONS.keys():
        group, _ = Group.objects.get_or_create(name=group_name)
        admin_group, _ = Group.objects.get_or_create(name="Admin")

        group_permission = GROUP_PERMISSIONS[group_name]

        for name, code_name in group_permission:
            permission, created = Permission.objects.get_or_create(name=name, codename=code_name,content_type=group_content_type)
            if created:
                pass
            group.permissions.add(permission)
            admin_group.permissions.add(permission)