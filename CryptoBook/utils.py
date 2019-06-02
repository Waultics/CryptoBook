from datetime import timedelta
from dateutil.parser import parse
import pandas as pd
import asyncio
import aiohttp
import ccxt

async def get_ip():
    """ Fetches and returns the external IP of the server for testing purposes. """

    # Grabs external IP address from ipify.org.
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get("https://api.ipify.org?format=json") as response:
            return await response.json()

# @todo Replace the market input var `ex` to `exchange` in 'exchange_info' function.
# @body For better code use it would be best to replace 'ex' with exchange.
async def exchange_info(ex):
    """ Fetches and returns relevant information about an exchange for historical data fetch.

    Args:
        ex (str): The name of the exchange.

    Returns:
        str: JSON data with market exchange information.
    """

    # Checks to see if the exchange is valid.
    try:
        exchange = getattr (ccxt, ex) ()
    except AttributeError:
        return {'error': 'exchange_error',
                'description': "Exchange {} not found. Please check the exchange is supported with ccxt.".format(ex)}

    # Loads the market.
    exchange.load_markets()

    # Returns the information.
    return { 'exchange': ex,
             'symbols': exchange.symbols,
             'timeframes': exchange.timeframes,
             'historical': exchange.has['fetchOHLCV']}

# @todo Replace the market input var 'ex' to 'exchange' in 'historical_data' function.
# @body For better code use it would be easier to have the `ex` param to be placed first, and be changed to `exchange`.
async def historical_data(symbol, ex, timeframe, start, end):
    """ Returns historical data of any market.

    Args:
        symbol (str): The exchange symbol one desires.
        ex (str): The name of the exchange.
        timeframe (str): Timeframe of the data.
        start (str): Beginning date and time of the data.
        end (str): Ending date and time of the data.

    Returns:
        str: JSON data with market exchange information.
    """

    # Checks to see if the exchange is valid.
    try:
        exchange = getattr (ccxt, ex) ()
    except AttributeError:
        return {'error': 'exchange_error',
                'description': "Exchange {} not found. Please check the exchange is supported.".format(ex)}

    # Checks if fetching of historical data for the specific exchange is allowed.
    if exchange.has["fetchOHLCV"] != True:
        return { 'error': 'historical_error',
                 'description': "{} does not support fetching OHLC data. Please use another exchange".format(ex)}

    # Checks to see if the timeframe is available.
    if (not hasattr(exchange, 'timeframes')) or (timeframe not in exchange.timeframes):
        return {'error': 'timeframe_error',
                'description': "The requested timeframe ({}) is not available from {}.".format(timeframe, ex),
                'timeframes': exchange.timeframes.keys()}

    # Loads the market.
    exchange.load_markets()
    exchange.enableRateLimit = False

    # Check to see if the symbol is available on the exchange.
    if symbol not in exchange.symbols:
        return { 'error': 'symbol_error',
                 'description': "The requested symbol ({}) is not available from {}.".format(symbol, ex),
                 'symbols': exchange.symbols}

    # Configuration settings for the DataFrame.
    header = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(columns=header)

    data_start = parse(start)
    data_end = parse(end)

    # Re-formats the `start` key to proper ISO8601.
    current = exchange.parse8601(parse(start).isoformat())

    # Begins while loop.
    while data_start < data_end:
        df = df.append(pd.DataFrame(data = exchange.fetch_ohlcv(symbol, timeframe, current), columns=header), ignore_index=True)

        current = df[-1:]['Time'].iloc[0]
        data_start = data_start + timedelta(microseconds=current)

    # Cuts off the DataFrame at the ending time.
    df = df[df.Time <= exchange.parse8601(data_end.isoformat())]

    return df.to_json()
