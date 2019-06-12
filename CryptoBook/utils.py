from datetime import timedelta
from dateutil.parser import parse
import pandas as pd
import cfscrape
import asyncio
import aiohttp

import ccxt
import ccxt.async_support as ccxt_async

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
        exchange_object (ccxt.Exchange): Optional ccxt.Exchange object with user-set configuration. If not passed, function will initialize a fresh ccxt.Exchange object.

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

    # @todo Make sure if exchange_object is passed, it is async.
    if exchange_object:
        ex = exchange_object
        ex.enableRateLimit = False
        ex.session = cfscrape.create_scraper()
    else:
        ex = getattr (ccxt_async, exchange) ()

    # Configuration settings for the DataFrame.
    header = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(columns=header)

    # Setting our start and ending variables as given by the input.
    time_start = ex.parse8601(parse(start).isoformat())
    time_end = ex.parse8601(parse(end).isoformat())

    # Getting the first DataFrame result to measure the size.
    resp_first = await ex.fetch_ohlcv(symbol, timeframe, time_start)

    # The interval of data in which the market is replying by.
    resp_interval = resp_first[-1][0] - resp_first[0][0]

    # Computes all of the datetime we must request from the exchange.
    times = []
    while time_start < time_end:
        time_start += resp_interval + 60000 # @todo make this dynamic to the interval given.
        times.append(time_start)

    # Create a DataFrame with the first response.
    df = df.append(pd.DataFrame(data = resp_first, columns=header), ignore_index=True)

    # Gathers all of the results in order.
    responses = await asyncio.gather(*[ex.fetch_ohlcv(symbol, timeframe, time) for time in times])

    # Appends all of our results to the DataFrame.
    dataframes = [pd.DataFrame(data = response, columns=header) for response in responses]
    df = df.append(dataframes, ignore_index=True)

    # Closes the connection with the exchange (required due to asynchronous support).
    await ex.close()

    # @todo Ensure that the time is not getting cut-off for other exchanges.
    # @desc This is due to parse8601 and the manner in which the specific market returns a timestamp. Ensure correct parser is being used.

    # Cuts off the DataFrame at the ending time.
    df = df[df.Time <= time_end]

    # Removes duplicates due to server responding with more values per call.
    df = df.drop_duplicates(keep='first')

    # Return the DataFrame as a dictionary.
    return df.to_dict()
