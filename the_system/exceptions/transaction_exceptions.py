from django.core import exceptions

class InvalidTransactionAmount(exceptions.BadRequest):
    pass


class  TransactionNotConfigured(exceptions.ObjectDoesNotExist):
    pass