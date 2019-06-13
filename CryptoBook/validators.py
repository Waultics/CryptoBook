from cerberus import Validator
from datetime import datetime
import ccxt.async_support as ccxt_async


async def check_exchange_info(exchange):
    """ Checks to see if the exchange is valid.

    Args:
        exchange (str): The name of the exchange to check.

    :returns:
        - **valid_request** (*bool*): Boolean representing whether or not check was successfull or failure.
        - **status** (*int*): HTTP code corresponding to the data validation. None if return bool above is true.
        - **response** (*dict*): The response by the validator; details about an error.
    """

    try:
        ex = getattr(ccxt_async, exchange)()
    except AttributeError:
        return (
            False,
            400,
            {
                "error": "exchange_error",
                "description": "Exchange {} not found. Please check the exchange is supported with ccxt.".format(
                    exchange
                ),
            },
        )

    # Closing connection with the market.
    await ex.close()

    return True, None, None


async def check_historical_data(request):
    """ Verify json request for /api/v1/cryptobook/historical endpoint.

    Args:
        request (dict): The request sent into the server.

    :returns:
        - **valid_request** (*bool*): Boolean representing whether or not check was successfull or failure.
        - **status** (*int*): HTTP code corresponding to the data validation. None if return bool above is true.
        - **response** (*dict*): The response by the validator; details about an error.
    """

    # @todo Add validation for fetchOHLCV function.
    # @description Due to the nature of some exchanges, their reply is not always historical. Therefore, there needs to be a manner in which the verifier checks to ensure the market will _only_ return the proper historical data asked by the user.

    # Creates the validator class and schema to check the requests' params.
    v = Validator()
    date = lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    v.schema = {
        "exchange": {"type": "string", "required": True},
        "symbol": {"type": "string", "required": True},
        "timeframe": {"type": "string", "required": True},
        "start": {"type": "datetime", "coerce": date, "required": True},
        "end": {"type": "datetime", "coerce": date, "required": True},
        "cfbypass": {"type": "boolean"},
    }

    # Checks to make sure the request has the proper keys.
    if not v.validate(request):
        return (
            False,
            400,
            {
                "error": "invalid_request",
                "description": "The server received the request, but the request was invalid.",
                "keys": v.errors,
            },
        )

    # Settings variables that will be checked by ccxt exchange params below.
    exchange = request["exchange"]
    symbol = request["symbol"]
    timeframe = request["timeframe"]

    # Checks to see if the exchange is valid.
    try:
        ex = getattr(ccxt_async, exchange)()
    except AttributeError:
        return (
            False,
            400,
            {
                "error": "exchange_error",
                "description": "Exchange {} not found. Please check the exchange is supported.".format(
                    exchange
                ),
            },
        )

    # Checks if fetching of historical data for the specific exchange is allowed.
    if ex.has["fetchOHLCV"] != True:
        return (
            False,
            400,
            {
                "error": "historical_error",
                "description": "{} does not support fetching OHLC data. Please use another exchange".format(
                    exchange
                ),
            },
        )

    # Checks to see if the timeframe is available.
    if (not hasattr(ex, "timeframes")) or (timeframe not in ex.timeframes):
        return (
            False,
            400,
            {
                "error": "timeframe_error",
                "description": "The requested timeframe ({}) is not available from {}.".format(
                    timeframe, exchange
                ),
                "timeframes": ex.timeframes.keys(),
            },
        )

    # Loads the market for the symbols.
    await ex.load_markets()

    # Check to see if the symbol is available on the exchange.
    if symbol not in ex.symbols:
        return (
            False,
            400,
            {
                "error": "symbol_error",
                "description": "The requested symbol ({}) is not available from {}.".format(
                    symbol, exchange
                ),
                "symbols": ex.symbols,
            },
        )

    # Closing connection with the market.
    await ex.close()

    # Returns true if all the checks passes with the loaded exchange.
    return True, None, None
