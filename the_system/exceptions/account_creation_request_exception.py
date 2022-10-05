from django.core import exceptions

class DuplicateAccountNumber(exceptions.BadRequest):
    pass