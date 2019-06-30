from utils import get_ip, get_exchange_info, get_historical_data
from errors import ExchangeDataAccuracyError, NetworkError

from cerberus import Validator
from datetime import datetime
import ccxt.async_support as ccxt_async


async def handle(func, *args, **kwargs):  # pragma: no cover
    """ Function to handle internal server errors.

        args:
            func (function): Function that will be called safely.
            *args: Unnamed variables to be called by func.
            **kwargs: Named variables to be called by func.
    """

    try:
        resp = await func(*args, **kwargs)
    except ExchangeDataAccuracyError as e:
        return {"error": "exchange_data_accuracy_error", "description": str(e)}, 400
    except NetworkError as e:  # pragma: no cover
        return {"error": "network_error", "description": str(e)}, 400
    except Exception as e:  # pragma: no cover
        return {"error": "server_error", "description": str(e)}, 400
    return resp, 200


async def ip():
    """  Safely grabs the IP of the microservice.

    :returns:
        - **response** (*dict*): Server response.
        - **status** (*int*): Server response HTTP status code.
    """

    # Handles and safely returns result.
    return await handle(get_ip)


async def exchange_info(request):
    """ Safely grabs the exchange information.

    Args:
        request (str): The request sent into the server.

    :returns:
        - **response** (*dict*): Server response.
        - **status** (*int*): Server response HTTP status code.
    """

    # In this case the request sent is the exchange's name.
    exchange = request

    try:
        # Opening ccxt exchange instance with async support.
        ex = getattr(ccxt_async, exchange)()
    except AttributeError:
        return (
            {
                "error": "exchange_error",
                "description": "Exchange {} not found. Please check the exchange is supported with ccxt.".format(
                    exchange
                ),
            },
            400,  # Bad Request
        )

    # Closing connection with the exchange.
    await ex.close()

    # Handles and safely returns result.
    return await handle(get_exchange_info, exchange=exchange)


async def historical_data(request):
    """ Safely grabs historical data.

    Args:
        request (dict): The request sent into the server.

    :returns:
        - **response** (*dict*): Server response.
        - **status** (*int*): Server response HTTP status code.
    """

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
            {
                "error": "invalid_request",
                "description": "The server received the request, but the request was invalid.",
                "keys": v.errors,
            },
            400,
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
            {
                "error": "exchange_error",
                "description": "Exchange {} not found. Please check the exchange is supported.".format(
                    exchange
                ),
            },
            400,
        )

    # Checks if fetching of historical data for the specific exchange is allowed.
    if ex.has["fetchOHLCV"] != True:
        return (
            {
                "error": "historical_error",
                "description": "{} does not support fetching OHLC data. Please use another exchange".format(
                    exchange
                ),
            },
            400,
        )

    # Checks to see if the timeframe is available.
    if (not hasattr(ex, "timeframes")) or (timeframe not in ex.timeframes):
        return (
            {
                "error": "timeframe_error",
                "description": "The requested timeframe ({}) is not available from {}.".format(
                    timeframe, exchange
                ),
                "timeframes": ex.timeframes.keys(),
            },
            400,
        )

    # Loads the market for the symbols.
    await ex.load_markets()

    # Check to see if the symbol is available on the exchange.
    if symbol not in ex.symbols:
        return (
            {
                "error": "symbol_error",
                "description": "The requested symbol ({}) is not available from {}.".format(
                    symbol, exchange
                ),
                "symbols": ex.symbols,
            },
            400,
        )

    # Closing connection with the market.
    await ex.close()

    # Handles and safely returns result.
    return await handle(get_historical_data, **request)
