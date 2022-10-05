import math
from decimal import *
from djmoney.money import Money
import traceback
import logging
logger = logging.getLogger('ilogger')

ZERO_DOLLAR = Money(0,"USD")
ONE_DOLLAR = Money(1,"USD")

# -------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------
def USD(amount, round_down=True):
 
    # logger.debug(f"amount 1 ----> ${amount}")
    if is_money(amount):
        try :
            amount= Decimal(str(amount).replace("$",'').replace(",",'').replace("US",''))
        except Exception as e:
            logger.error(f"{e} : {traceback.format_exc()}")
            raise e


    if round_down:
        amount = round_decimals_down(amount,2)
 

    return Money(amount,'USD',decimal_places=3, decimal_places_display=3 ) 


# -------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------
def is_money(amount):
    return isinstance(amount,Money)

# -------------------------------------------------------------------------------------------
#
# -------------------------------------------------------------------------------------------


def round_decimals_down(number:float, decimals:int=2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals 
    number_as_money = Money(number,'USD')
    number_to_floor = number_as_money*factor
    return math.floor(number_to_floor.amount) / factor


def round_decimals_up(number:float, decimals:int=2):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor