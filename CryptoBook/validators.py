from cerberus import Validator, DocumentError
from datetime import datetime

from sanic.response import json
import ccxt

def check_historical_data(request):
    """ Verify json request for /api/v1/cryptobook/historical endpoint.

    Args:
        request (dict): The request sent into the server.

    Returns:
        bool: Boolean representing whether or not check was successfull or failure.
        dict: Errors corresponding to the data validation. Empty if return bool is true.
    """

    # Creates the validator class and schema to check the requests' params.
    v = Validator()
    date = lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    v.schema = {'exchange': {'type': 'string'},
                'symbol': {'type': 'string'},
                'timeframe': {'type': 'string'},
                'start': {'type': 'datetime', 'coerce': date},
                'end': {'type': 'datetime', 'coerce': date}}

    # Checks to make sure the request has the proper keys.
    try:
        if v.validate(request) is False:
            return False, json({'error': 'invalid_request',
                                'description': 'The server received the request, but the request was invalid.',
                                'keys': v.errors},
                                status=400)
    except DocumentError:
        return False, json({'error': 'document_missing',
                            'description': 'The server received the request, but the request did not contain data.'},
                            status=400)

    # Settings variables that will be checked by ccxt exchange params below.
    exchange = request['exchange']
    symbol = request['symbol']
    timeframe = request['timeframe']

    # Checks to see if the exchange is valid.
    try:
        ex = getattr (ccxt, exchange) ()
    except AttributeError:
        return False, json({'error': 'exchange_error',
                            'description': "Exchange {} not found. Please check the exchange is supported.".format(exchange)},
                            status=400)

    # Checks if fetching of historical data for the specific exchange is allowed.
    if ex.has["fetchOHLCV"] != True:
        return False, json({'error': 'historical_error',
                            'description': "{} does not support fetching OHLC data. Please use another exchange".format(exchange)},
                            status=400)

    # Checks to see if the timeframe is available.
    if (not hasattr(ex, 'timeframes')) or (timeframe not in ex.timeframes):
        return False, json({'error': 'timeframe_error',
                            'description': "The requested timeframe ({}) is not available from {}.".format(timeframe, exchange),
                            'timeframes': ex.timeframes.keys()},
                            status=400)

    # Loads the market for the symbols.
    ex.load_markets()

    # Check to see if the symbol is available on the exchange.
    if symbol not in ex.symbols:
        return False, json({'error': 'symbol_error',
                            'description': "The requested symbol ({}) is not available from {}.".format(symbol, exchange),
                            'symbols': ex.symbols},
                            status=400)

    # Returns true if all the checks passes with the loaded exchange.
    return True, {'exchange-object': ex}
