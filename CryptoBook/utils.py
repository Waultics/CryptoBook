from datetime import timedelta
from dateutil.parser import parse
import pandas as pd
import asyncio
import aiohttp

import ccxt.async_support as ccxt_async
import ccxt
import cfscrape

async def get_ip():
    """ Fetches and returns the external IP of the server for testing purposes. """

    # Grabs external IP address from ipify.org.
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get("https://api.ipify.org?format=json") as response:
            return await response.json()

async def exchange_info(exchange):
    """ Fetches and returns relevant information about an exchange for historical data fetch.

    Args:
        exchange (str): The name of the exchange.

    Returns:
        str: JSON data with market exchange information.
    """

    # Loads the market.
    ex = getattr (ccxt_async, exchange) ()

    # Loads the market.
    await ex.load_markets()

    # Returns the information.
    return { 'exchange': exchange,
             'symbols': ex.symbols,
             'timeframes': ex.timeframes,
             'historical': ex.has['fetchOHLCV']}

async def historical_data(exchange, symbol, timeframe, start, end, cfbypass=False):
    """ Returns historical data of any market.

    Args:
        ex (ccxt.Exchange): Exchange object.
        symbol (str): The exchange symbol one desires.
        timeframe (str): Timeframe of the data.
        start (str): Beginning date and time of the data.
        end (str): Ending date and time of the data.
        cfbypass (bool): Optional flag to indicated whether or not do bypass CloudFlare checks (read notes).

    Returns:
        str: JSON data with market exchange information.

    Note:
        Due to cfscrape lack of asynchronous support this function must be split into two different
        functionalities: (1) one which does not support full async gathering and uses cfscrape to bypass
        CloudFlare checking mechanism, and (2) one that supports asynchronous calls but does not attempt to
        bypass CloudFlare mechanism.
    """

    # Loadst the market.
    if cfbypass:
        ex = getattr (ccxt, exchange) ({
            'session': cfscrape.create_scraper(),
            'enableRateLimit': False
        })
    else:
        ex = getattr (ccxt_async, exchange) ({
            'enableRateLimit': False
        })

    # Configuration settings for the DataFrame.
    header = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame(columns=header)

    # @todo Ensure that the time is not getting cut-off for other exchanges.
    # @desc This is due to parse8601 and the manner in which the specific market returns a timestamp. Ensure correct parser is being used.

    # Setting our start and ending variables as given by the input.
    time_start = ex.parse8601(parse(start).isoformat())
    time_end = ex.parse8601(parse(end).isoformat())

    # Getting the first DataFrame result to measure the size.
    if cfbypass:
        resp_first = ex.fetch_ohlcv(symbol, timeframe, time_start)
    else:
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
    if cfbypass:
        responses = [ex.fetch_ohlcv(symbol, timeframe, time) for time in times]
    else:
         responses = await asyncio.gather(*[ex.fetch_ohlcv(symbol, timeframe, time) for time in times])

    # Appends all of our results to the DataFrame.
    dataframes = [pd.DataFrame(data = response, columns=header) for response in responses]
    df = df.append(dataframes, ignore_index=True)

    # Cuts off the DataFrame at the ending time.
    #df = df[df.Time <= time_end]

    # Removes duplicates due to server responding with more values per call.
    df = df.drop_duplicates(keep='first')

    if not cfbypass:
        await ex.close()

    # Return the DataFrame as a dictionary.
    return df.to_dict()
