from errors import ExchangeDataAccuracyError, NetworkError

from dateutil.parser import parse
import ccxt.async_support as ccxt_async
import ccxt
import cfscrape
import pandas as pd
import asyncio
import aiohttp


async def get_ip():
    """ Fetches and returns the external IP of the server for testing purposes. """

    # Grabs external IP address from ipify.org.
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(
            "https://api.ipify.org?format=json", ssl=False
        ) as response:
            resp = await response.read()

        return {"ip": resp}


async def get_exchange_info(exchange):
    """ Fetches and returns relevant information about an exchange for historical data fetch.

    Args:
        exchange (str): The name of the exchange.

    Returns:
        str: JSON data with market exchange information.
    """

    # Loads the market.
    ex = getattr(ccxt_async, exchange)()

    # Loads the market.
    await ex.load_markets()

    # Gathers market data.
    data = {
        "exchange": exchange,
        "symbols": ex.symbols,
        "timeframes": ex.timeframes,
        "historical": ex.has["fetchOHLCV"],
    }

    # Closes the market connection due to async ccxt.
    await ex.close()

    # Returns the information.
    return data


async def get_historical_data(exchange, symbol, timeframe, start, end, cfbypass=False):
    """ Returns historical data of any market.

    Args:
        ex (ccxt.Exchange): Exchange object.
        symbol (str): The exchange symbol one desires.
        timeframe (str): Timeframe of the data.
        start (str): Beginning date and time of the data.
        end (str): Ending date and time of the data.
        cfbypass (bool): Optional flag to indicated whether or not do bypass CloudFlare checks (read notes).

    Returns:
        dict: Dictionary with the market history.

    Note:
        Due to cfscrape lack of asynchronous support this function must be split into two different
        functionalities: (1) one which does not support full async gathering and uses cfscrape to bypass
        CloudFlare checking mechanism, and (2) one that supports asynchronous calls but does not attempt to
        bypass CloudFlare mechanism.
    """

    # Loads the market.
    if cfbypass:
        # Creates ccxt instance with cfscrape as session.
        ex = getattr(ccxt, exchange)(
            {
                "session": cfscrape.create_scraper(),
                "enableRateLimit": False,
                "verify": False,
                "trust_env": True,
                "timeout": 60000,
            }
        )
    else:
        # Creates asyhronous ccxt instance.
        ex = getattr(ccxt_async, exchange)(
            {
                "enableRateLimit": False,
                "verify": False,
                "aiohttp_trust_env": True,
                "timeout": 60000,
            }
        )

    # Configuration settings for the DataFrame.
    header = ["Time", "Open", "High", "Low", "Close", "Volume"]
    df = pd.DataFrame(columns=header)

    # Setting our start and ending variables as given by the input.
    time_start = ex.parse8601(parse(start).isoformat())
    time_end = ex.parse8601(parse(end).isoformat())

    # Creates copy of time_start for later check (since time_start changes).
    time_start_copy = time_start

    # Getting the first DataFrame result to measure the size.
    try:
        if cfbypass:
            resp_first = ex.fetch_ohlcv(symbol, timeframe, time_start)
        else:
            resp_first = await ex.fetch_ohlcv(symbol, timeframe, time_start)
    except ccxt.NetworkError as e:  # pragma: no cover
        await ex.close()
        raise NetworkError("Error loading the data. {}".format(e))

    # The interval of data in which the market is replying by.
    resp_interval = resp_first[-1][0] - resp_first[0][0]

    # Retrieves the smaller interval between two side-by-side data points.
    resp_small_interval = resp_first[-1][0] - resp_first[-2][0]

    # Computes all of the datetime we must request from the exchange.
    times = []
    while time_start < time_end:
        time_start += resp_interval + resp_small_interval
        times.append(time_start)

    # Create a DataFrame with the first response.
    df = df.append(pd.DataFrame(data=resp_first, columns=header), ignore_index=True)

    try:
        # Gathers all of the results in order.
        if cfbypass:
            responses = [ex.fetch_ohlcv(symbol, timeframe, time) for time in times]
        else:
            responses = await asyncio.gather(
                *[ex.fetch_ohlcv(symbol, timeframe, time) for time in times]
            )
    except ccxt.NetworkError as e:  # pragma: no cover
        await ex.close()
        raise NetworkError("Error loading the data. {}".format(e))
    except Exception as e:  # pragma: no cover
        await ex.close()
        raise Exception("Unknown error occured. {}".format(e))

    # Appends all of our results to the DataFrame.
    dataframes = [pd.DataFrame(data=response, columns=header) for response in responses]
    df = df.append(dataframes, ignore_index=True)

    # Removes duplicates due to server responding with (sometimes) duplicate values.
    df = df.drop_duplicates(keep="first")

    # Must close connection with market if using ccxt asynchronously.
    if not cfbypass:
        await ex.close()

    # Saves the first and last time in the DataFrame.
    first_time = df.iloc[0]["Time"]
    last_time = df.iloc[-1]["Time"]

    # Raise error if the first time in the DataFrame is inaccurate by more than 1%.
    if (
        not abs(first_time - time_start_copy) < time_start_copy * 0.01
    ):  # pragma: no cover
        raise ExchangeDataAccuracyError(
            "Could not retrieve dates from this exchange."
            "Server responded with a different time start range."
        )

    # Raise error if the last time in the DataFrame is inaccurate by more than 1%.
    if not abs(last_time - time_end) < time_end * 0.01:  # pragma: no cover
        raise ExchangeDataAccuracyError(
            "Could not retrieve dates from this exchange."
            "Server responded with a different time end range."
        )

    # Cuts off the DataFrame at the ending time.
    df = df[df.Time <= time_end]

    # Return the DataFrame as a dictionary.
    return df.to_dict(orient="split")
