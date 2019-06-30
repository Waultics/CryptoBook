from CryptoBook import handlers


class Test_exchange_info(object):
    """ Test for exchange_info() function with improper params. """

    async def test_invalid_input(self):
        response, status = await handlers.exchange_info("random")
        assert response.keys() == set(["error", "description"])
        assert status == 400


class Test_historical_data(object):
    """ Test for the historical_data() function with improper and empty params. """

    async def test_empty_input(self):
        """ Checking empty input returns false and proper return. """
        data = {}
        response, status = await handlers.historical_data(data)
        assert response["error"] == "invalid_request"
        assert status == 400

    async def test_partial_data(self):
        """ Checking partial data returns false and proper return. """
        data = {"exchange": "binance"}
        response, status = await handlers.historical_data(data)
        assert response["error"] == "invalid_request"
        assert status == 400

    async def test_unknown_exchange(self):
        """ Checking if exchange name is unknown, it returns proper error. """
        data = {
            "exchange": "random_unknown_name",
            "symbol": "ETH/BTC",
            "timeframe": "1m",
            "start": "2018-01-01 00:00:00",
            "end": "2018-05-01 00:00:00",
        }
        response, status = await handlers.historical_data(data)
        assert response["error"] == "exchange_error"
        assert status == 400

    async def test_exchange_support_for_historical_data(self):
        """ Checking to see if valid exchange with no support for historical data. """
        data = {
            "exchange": "coinmarketcap",
            "symbol": "ETH/BTC",
            "timeframe": "1m",
            "start": "2018-01-01 00:00:00",
            "end": "2018-05-01 00:00:00",
        }
        response, status = await handlers.historical_data(data)
        assert response["error"] == "historical_error"
        assert status == 400

    async def test_exchange_support_for_timeframe(self):
        """ Checking if valid exchange has support for the given timeframe. """
        data = {
            "exchange": "binance",
            "symbol": "ETH/BTC",
            "timeframe": "2m",
            "start": "2018-01-01 00:00:00",
            "end": "2018-05-01 00:00:00",
        }
        response, status = await handlers.historical_data(data)
        assert response["error"] == "timeframe_error"
        assert status == 400

    async def test_exchange_support_for_symbol(self):
        """ Checking if valid exchange has support for the given symbol. """
        data = {
            "exchange": "binance",
            "symbol": "ETH/USD",
            "timeframe": "1m",
            "start": "2018-01-01 00:00:00",
            "end": "2018-05-01 00:00:00",
        }
        response, status = await handlers.historical_data(data)
        assert response["error"] == "symbol_error"
        assert status == 400
