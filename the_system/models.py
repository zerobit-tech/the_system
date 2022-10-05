from tabnanny import verbose
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
import uuid 
from .middleware import get_current_user
import logging
logger = logging.getLogger('ilogger')
class BaseModel(models.Model):
#    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, default=get_current_user, on_delete=models.DO_NOTHING, related_name="%(app_label)s_%(class)s_created")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created On"))
    modified_date = models.DateTimeField(auto_now=True, verbose_name=_("Modified on"))   
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True



# custom permissions

# class RightsSupport(models.Model):
            
#     class Meta:
        
#         managed = False  # No database table creation or deletion  \
#                          # operations will be performed for this model. 
                
#         default_permissions = () # disable "add", "change", "delete"
#                                  # and "view" default permissions

#         permissions = ( 
#             ('customer_rights', 'Global customer rights'),  
#             ('vendor_rights', 'Global vendor rights'), 
#             ('any_rights', 'Global any rights'), 
#         )


# Create your models here.

class SystemConfig(models.Model):
    class Config(models.TextChoices):
        APP_NAME = 'APP_NAME', _('APPLICATION NAME')
        # SITE_HEADER = 'SITE_HEADER', _('ADMIN SITE HEADER')
        # SITE_TITLE = 'SITE_TITLE', _('ADMIN SITE TITLE')
        # INDEX_TITLE = 'INDEX_TITLE', _('ADMIN SITE INDEX TITLE')
        # POWERED_BY = 'POWERED_BY', _('POWERED BY WEBSITE')
        # ACTIVATE_BATCH_TRANSACTION_POSTING = 'BATCH_TRANSATION_POSTING', _('BATCH TRANSATION POSTING')

    config = models.CharField(max_length=25, primary_key=True, verbose_name="Configuration Name",
                              choices=Config.choices)
    value = models.CharField(max_length=100, verbose_name="Value")

    class Meta:
        verbose_name = "System Configuration"

    def __str__(self):
        return self.config

    @staticmethod
    def get(config):
        config = str(config).upper()
        try:
            config_object = SystemConfig.objects.get(config=config)
        except SystemConfig.DoesNotExist:
            return ""

        if config_object:
            return config_object.value

        return ""