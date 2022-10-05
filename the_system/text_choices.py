from http.client import PROCESSING
from django.db import models

from django.utils.translation import gettext as _
import logging
logger = logging.getLogger('ilogger')

US_STATES = (
    ('AL', _('Alabama')),
    ('AZ', _('Arizona')),
    ('AR', _('Arkansas')),
    ('CA', _('California')),
    ('CO', _('Colorado')),
    ('CT', _('Connecticut')),
    ('DE', _('Delaware')),
    ('DC', _('District of Columbia')),
    ('FL', _('Florida')),
    ('GA', _('Georgia')),
    ('ID', _('Idaho')),
    ('IL', _('Illinois')),
    ('IN', _('Indiana')),
    ('IA', _('Iowa')),
    ('KS', _('Kansas')),
    ('KY', _('Kentucky')),
    ('LA', _('Louisiana')),
    ('ME', _('Maine')),
    ('MD', _('Maryland')),
    ('MA', _('Massachusetts')),
    ('MI', _('Michigan')),
    ('MN', _('Minnesota')),
    ('MS', _('Mississippi')),
    ('MO', _('Missouri')),
    ('MT', _('Montana')),
    ('NE', _('Nebraska')),
    ('NV', _('Nevada')),
    ('NH', _('New Hampshire')),
    ('NJ', _('New Jersey')),
    ('NM', _('New Mexico')),
    ('NY', _('New York')),
    ('NC', _('North Carolina')),
    ('ND', _('North Dakota')),
    ('OH', _('Ohio')),
    ('OK', _('Oklahoma')),
    ('OR', _('Oregon')),
    ('PA', _('Pennsylvania')),
    ('RI', _('Rhode Island')),
    ('SC', _('South Carolina')),
    ('SD', _('South Dakota')),
    ('TN', _('Tennessee')),
    ('TX', _('Texas')),
    ('UT', _('Utah')),
    ('VT', _('Vermont')),
    ('VA', _('Virginia')),
    ('WA', _('Washington')),
    ('WV', _('West Virginia')),
    ('WI', _('Wisconsin')),
    ('WY', _('Wyoming')),
    ('AK', _('Alaska')),
    ('HI', _('Hawaii')),
)

 
class AccountCreationRequestStatus(models.TextChoices):
        PENDING = 'P', _('Pending')
        COMPLETED = 'C', _('Completed')
        ERROR = 'E', _('Error')
class CalculationTypes(models.TextChoices):
        FIXEDAMOUNT = 'F', _('Fixed Amount')
        RATE = 'R', _('Rate or Percentage')
        SPECIAL = 'S', _('Special Calculation')


class CommnucationTypes(models.TextChoices):
        EMAIL = 'E', _('Email')
        PHONE = 'P', _('Phone or Cell')
        MAIL = 'M', _('Postal Mail ')


class AutoPayAmountOptions(models.TextChoices):
        MINIMUM_AMOUNT_DUE = 'M' , _('Minimum Amount due') 
        TOTAL_AMOUNT_DUE = 'T', _('Total amount due')

class Frequencies(models.TextChoices):
        WEEKLY = 'W', _('Weekly')
        BI_WEEKLY = 'B', _('BI-Weekly')
        SEMI_MONTHLY = 'T', _('Twice Montly')
        MONTHLY = 'M', _('Monthly')
       

class AddressTypes(models.TextChoices):
        HOME = 'H', _('Home')
        SHIPPING = 'S', _('Shipping')
        OFFICE = 'O', _('Office')
        BILLING = 'B', _('Billing')
        MAILING = 'M', _('MAILING')

class CardTypes(models.TextChoices):
        DEBIT = 'D', _('Debit')
        CREDIT = 'C', _('Credit')

class BankAccountsTypes(models.TextChoices):
        SAVING = 'S', _('Saving')
        CHECKING = 'C', _('Checking')



class TransactionTypes(models.TextChoices):
        OPEN_ACCOUNT='open_account',_('Open Account')
        NEW_BILLING_CYCLE = 'new_billing_cycle',_('New Billing Cycle')
        CLOSE_ACCOUNT='close_account',_('Close Account')
        
        CASH_ADVANCE='cash_advance',_('Cash Advance')
        ADJUST_CASH_ADVANCE_FEE ='adjust_cash_advance_fee', _('Adjust cash advance fee')
        # REVERSE_CASH_ADVANCE = 'reverse_cash_advance', _('Reverse Cash Advance') # TODO
        # REVERSE_CASH_ADVANCE_FEE = 'reverse_cash_advance_fee', _('Reverse Cash Advance Fee') # TODO
        
        PAYMENT='payment',_('Payment')
        CREDIT_LIMIT_ADJUSTMENT= 'credit_limit_adjustment',_('Credit limit adjustment')
        EPD_PAYMENT='epd_payment',_('EPD Payment')
        REVERSE_PAYMENT = 'reverse_payment', _('Reverse Payment')

        START_EPD_CYCLE = 'start_epd_cycle', _('Start EPD Cycle')
        END_EPD_CYCLE = 'end_epd_cycle', _('End EPD Cycle')

        CARRIED_BALANCE_FEE='carried_balance_fee',_('Carried Balance fee')
        ADJUST_CARRIED_BALANCE_FEE ='adjust_carried_balance_fee', _('Adjust carried balance fee')
        STATEMENT = 'statement', _('Statement')

        LATE_FEE ='late_fee', _('Late Fee')
        REVERSE_LATE_FEE ='reverse_late_fee', _('Reverse Late Fee')
        ADJUST_LATE_FEE ='adjust_late_fee', _('Adjust Late Fee')

        NSF_FEE = 'nsf_fee', _('NSF Fee')
        REVERSE_NSF_FEE ='reverse_nsf_fee', _('Reverse NSF Fee')

        CREDIT = 'credit', _('Credit'),
        # PRINCIPAL_CREDIT  = 'principal credit', _('Principal Credit'),


        CHECK_ACCOUNT_DUE ='check_account_due', _('Check account due')
        
        FREQUENCY_CHANGE_REQUEST ='frequency_change_request', _('Frequency change request')
        FREQUENCY_CHANGE ='frequency_change', _('Frequency change')


        AUTOPAY_ENABLED = 'autopay_enabled', _('Autopay enabled')
        AUTOPAY_DISABLED = 'autopay_disabled', _('Autopay disabled')

        AUTO_PAYMENT = 'auto_payment', _('Auto payment')
        
        DUE_DATE_NOTICE = 'due_date_notice', _('Due Date notice')
        CREDIT_REPORTING = 'credit_reporting', _('Credit report')

        @classmethod
        def as_dict(cls):
            return dict(TransactionTypes.choices)

class AccountCreationStatus(models.TextChoices):
        PENDING = 'P', _('Pending')
        COMPLETED = 'C', _('Completed')
        ERROR = 'E', _('Error')


class TransactionStatus(models.TextChoices):
        PENDING = '-',_('Pending'),
        POSTED = 'P',_('Posted'),
        REVERESED = 'R',_('Reversed')
        ERROR = 'E',_('Error')
        @classmethod
        def as_dict(cls):
            return dict(TransactionStatus.choices)

class EPDCycleStatus(models.TextChoices):
        ACTIVE = 'A',_('Active'),
        EXPIRED = 'E', _('Expired')
        USED = 'U' , _('Used')


class NoteTypes(models.TextChoices):
        NOTHING = ' ', _('Nothing')
        WARNING = 'W', _('Warning')
        ERROR = 'E', _('Error')
        CALCULATION = 'C', _('Calculation')

class AccountStatus(models.TextChoices):
        PENDING = 'P', _('Pending'),
        OPEN = 'O', _('Open'),
        CLOSE = 'C', _('Closed'),
        WRITEOFF = 'W', _('Write-Off'),


class EmailStatus(models.TextChoices):
        PENDING = 'P', _('Pending'),
        SENT = 'S', _('Sent'),
        ERROR = 'E', _('Error'),

class EmailGroups(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin'),
        LEGAL = 'LEGAL', _('Legal'),
        COMPILANCE = 'COMPLIANCE', _('Compilance'),
        ACCOUNTS = 'ACCOUNTS', _('Accounts'),


        @classmethod
        def as_dict(cls):
                return dict(EmailGroups.choices)

class ScheduledPaymentStatus(models.TextChoices):
        PENDING = 'P', _('Pending'),
        COMPLETE = 'C', _('Completed'),
        ERROR = 'E', _('Error'),


class UserLanguages(models.TextChoices):
        ENGLISH = 'en', _('English'),
        SPANISH = 'es', _('Spanish'),
        HINDI = 'hi', _('Hindi'),



class StatementStatus(models.TextChoices):
        PENDING = '', _('Pending')
        PRINTED = 'P', _('Printed')
        ERROR = 'E', _('Error')
 

class BillinCycleEvents(models.TextChoices):

        PENDING = 'P', _('Pending'),
        PROCESSING = 'R', _('Processing'),
        COMPLETE = 'C', _('Completed'),
        ERROR = 'E', _('Error'),
