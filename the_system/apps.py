from django.apps import AppConfig
import os
import traceback
import logging

logger = logging.getLogger('ilogger')
class TheSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'the_system'

    def ready(self):
        from . import signals
        from . import signals_handlers
        
        # try:
             
        #     from .initial_load import create_initial_user_groups,create_initial_permissions, create_service_user
        #     create_service_user()
        #     create_initial_user_groups()
        #     create_initial_permissions()
        # except Exception as e:
        #     logger.error(f"Error loading initial data {e}: {traceback.format_exc()}")
        #     pass

        # from .models import SystemConfig
        # from django.contrib import admin
        # app_name = SystemConfig.get(SystemConfig.Config.APP_NAME.name)
        # site_header = SystemConfig.get("site_header")
        # site_title = SystemConfig.get("site_title")
        # index_title = SystemConfig.get("index_title")
        #
        # admin.site.site_header = site_header if site_header else app_name
        # admin.site.site_title = site_title if site_title else app_name
        # admin.site.index_title = index_title if index_title else app_name
