from datetime import datetime, timedelta
from dateutil.parser import parse
import pandas as pd
import asyncio
import ccxt

async def scraper_historical_data(symbol, ex, timeframe, start, end):
    """ Returns historical data of any market. """

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

    # Converts the df Timestamp column into DateTime objects.
    df['Time'] = pd.to_datetime(df['Time'], unit='ms')

    return df.to_json()
