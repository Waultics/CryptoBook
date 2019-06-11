from cerberus import Validator, DocumentError
from datetime import datetime

from sanic.response import json
import ccxt

def check_exchange_info(exchange):
    """ Checks to see if the exchange is valid.

    Args:
        exchange (str): The name of the exchange to check.

    :returns:
        - **valid_request** (*bool*): Boolean representing whether or not check was successfull or failure.
        - **status** (*int*): HTTP code corresponding to the data validation. None if return bool above is true.
        - **response** (*dict*): The response by the validator; either an error, or the loaded ccxt exchange object.
    """

    try:
        ex = getattr (ccxt, exchange) ()
    except AttributeError:
        return False, 400, {'error': 'exchange_error',
                            'description': "Exchange {} not found. Please check the exchange is supported with ccxt.".format(exchange)}

    return True, None, {'exchange-object': ex}

def check_historical_data(request):
    """ Verify json request for /api/v1/cryptobook/historical endpoint.

    Args:
        request (dict): The request sent into the server.

    :returns:
        - **valid_request** (*bool*): Boolean representing whether or not check was successfull or failure.
        - **status** (*int*): HTTP code corresponding to the data validation. None if return bool above is true.
        - **response** (*dict*): The response by the validator; either an error, or the loaded ccxt exchange object.
    """

    # Creates the validator class and schema to check the requests' params.
    v = Validator()
    date = lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    v.schema = {'exchange': {'type': 'string', 'required': True},
                'symbol': {'type': 'string', 'required': True},
                'timeframe': {'type': 'string', 'required': True},
                'start': {'type': 'datetime', 'coerce': date, 'required': True},
                'end': {'type': 'datetime', 'coerce': date, 'required': True}}

    # Checks to make sure the request has the proper keys.
    if not v.validate(request):
        return False, 400, {'error': 'invalid_request',
                            'description': 'The server received the request, but the request was invalid.',
                            'keys': v.errors}

    # Settings variables that will be checked by ccxt exchange params below.
    exchange = request['exchange']
    symbol = request['symbol']
    timeframe = request['timeframe']

    # Checks to see if the exchange is valid.
    try:
        ex = getattr (ccxt, exchange) ()
    except AttributeError:
        return False, 400, {'error': 'exchange_error',
                            'description': "Exchange {} not found. Please check the exchange is supported.".format(exchange)}

    # Checks if fetching of historical data for the specific exchange is allowed.
    if ex.has["fetchOHLCV"] != True:
        return False, 400, {'error': 'historical_error',
                            'description': "{} does not support fetching OHLC data. Please use another exchange".format(exchange)}

    # Checks to see if the timeframe is available.
    if (not hasattr(ex, 'timeframes')) or (timeframe not in ex.timeframes):
        return False, 400, {'error': 'timeframe_error',
                            'description': "The requested timeframe ({}) is not available from {}.".format(timeframe, exchange),
                            'timeframes': ex.timeframes.keys()}

    # Loads the market for the symbols.
    ex.load_markets()

    # Check to see if the symbol is available on the exchange.
    if symbol not in ex.symbols:
        return False, 400, {'error': 'symbol_error',
                            'description': "The requested symbol ({}) is not available from {}.".format(symbol, exchange),
                            'symbols': ex.symbols}

    # Returns true if all the checks passes with the loaded exchange.
    return True, None, {'exchange-object': ex}
