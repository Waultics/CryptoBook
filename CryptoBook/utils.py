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

async def exchange_info(exchange, exchange_object=None):
    """ Fetches and returns relevant information about an exchange for historical data fetch.

    Args:
        exchange (str): The name of the exchange.

    Returns:
        str: JSON data with market exchange information.
    """

    if exchange_object:
        ex = exchange_object
    else:
        ex = getattr (ccxt, exchange) ()

    # Loads the market.
    ex.load_markets()

    # Returns the information.
    return { 'exchange': exchange,
             'symbols': ex.symbols,
             'timeframes': ex.timeframes,
             'historical': ex.has['fetchOHLCV']}

async def historical_data(exchange, symbol, timeframe, start, end, exchange_object=None):
    """ Returns historical data of any market.

    Args:
        ex (ccxt.Exchange): Exchange object.
        symbol (str): The exchange symbol one desires.
        timeframe (str): Timeframe of the data.
        start (str): Beginning date and time of the data.
        end (str): Ending date and time of the data.
        exchange_object (ccxt.Exchange): Optional ccxt.Exchange object with user-set configuration. If not passed, function will initialize a fresh ccxt.Exchange object.

    Returns:
        str: JSON data with market exchange information.
    """

    if exchange_object:
        ex = exchange_object
        ex.enableRateLimit = False
    else:
        ex = getattr (ccxt, exchange) ()

    # Configuration settings for the DataFrame.
    header = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(columns=header)

    data_start = parse(start)
    data_end = parse(end)

    # Re-formats the `start` key to proper ISO8601.
    current = ex.parse8601(parse(start).isoformat())

    # Begins while loop.
    while data_start < data_end:
        df = df.append(pd.DataFrame(data = ex.fetch_ohlcv(symbol, timeframe, current), columns=header), ignore_index=True)

        current = df[-1:]['Time'].iloc[0]
        data_start = data_start + timedelta(microseconds=current)

    # Cuts off the DataFrame at the ending time.
    df = df[df.Time <= ex.parse8601(data_end.isoformat())]

    return df.to_dict()
