API Documentation
==================

External IP
------------------

.. http:get:: /api/v1/cryptobook/ip

    Returns the IP address of the server (for checking/testing purposes).

    **Example request**:

    .. sourcecode:: http

        GET /api/v1/cryptobook/ip HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 21
        Content-Type: application/json
        Keep-Alive: 5

        {
            "ip": "31.23.52.17"
        }

Exchange Information
--------------------

.. http:get:: /api/v1/cryptobook/exchange/(string:exchange_name)

    Returns relevant information about the given market to be able to scrape historical data.

    **Example request**:

    .. sourcecode:: http

        GET /api/v1/cryptobook/exchange/binance HTTP/1.1

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Connection: keep-alive
        Content-Length: 6400
        Content-Type: application/json
        Keep-Alive: 5

        {
           "exchange": "binance",
           "historical": true,
           "symbols": [
              "ADA/BNB",
              "...",
              "ZRX/USDT"
           ],
           "timeframes": {
              "12h": "12h",
              "...",
              "8h": "8h"
           }
        }

    :statuscode 200: No error.
    :statuscode 404: Resource not found.

Historical Data
---------------

.. http:post:: /api/v1/cryptobook/historical

    Returns historical exchange data from given params.

    **Example request**:

    .. sourcecode:: http

        POST /api/v1/cryptobook/historical HTTP/1.1
        Accept: application/json

        {
            "exchange": "binance",
            "symbol": "ETH/BTC",
            "timeframe": "1m",
            "start": "2018-01-01 00:00:00",
            "end": "2018-05-01 00:00:00"
        }

    :jsonparam string exchange: The name of the exchange.
    :jsonparam string symbol: The exchange symbol one desires.
    :jsonparam string timeframe: Timeframe of the data.
    :jsonparam string start: Beginning date and time of the data.
    :jsonparam string end: Ending date and time of the data.
    :statuscode 200: No error.
    :statuscode 404: Resource not found.

    **Parsing data**:

    Once you have received the data, the data is ready to be made back into a Pandas DataFrame.

    .. sourcecode:: python

        df = pd.read_json(resp)
