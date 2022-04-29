from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, ConnectionHandler, OperationalError, connections
from django.conf import settings
from copy import deepcopy
import re

import logging

LOGGER = logging.getLogger(__name__)

'''
python manage.py drop_db default
python manage.py drop_db pci

'''

class Command(BaseCommand):
    def handle(self, *args, **options):
        selected_database = options["database"]
        self.drop_db(selected_database)
    

    def add_arguments(self, parser):
        parser.add_argument('database',   type=str)

    def drop_db(self, database):
        database_vendor = connections[database].vendor
        # print("Creating db >>>>>>>>>>>>>>>",database_vendor,connections[database])
        if database_vendor == "postgresql":
            database_config = settings.DATABASES[database]
            postgres_database_config = deepcopy(database_config)
            postgres_database_config["NAME"] = "postgres"


            handler = ConnectionHandler(
                settings={DEFAULT_DB_ALIAS: postgres_database_config}
            )

            database_name = database_config["NAME"]
            with handler[DEFAULT_DB_ALIAS].cursor() as cursor:
                cursor.execute("DROP DATABASE \"{}\" WITH (FORCE)".format(database_name))

            self.stdout.write("DROP database '{}'".format(database_name))
            return True

        return False