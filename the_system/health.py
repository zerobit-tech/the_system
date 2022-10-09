
from the_system.decorators.health_check_provider import health_check_provider
from django.db.utils import OperationalError
from django.db import connections

@health_check_provider("Database Connections")
def check_db_connections(request):
    messages = []
    
    for connection in connections:
        print("connection  --", connection ,  type(connection))
        try:
            c = connections[connection].cursor()
            messages.append(f"Database {connection}: connection is up and running ")
        except OperationalError as e:
            return False, str(e)

    return True, messages


 
