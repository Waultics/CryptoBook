from CryptoBook import validators
from ccxt import Exchange
import pytest

class Test_check_exchange_info(object):
    """ Test for check_exchange_info() function with proper and improper params. """

    def test_proper_input(self):
        valid_request, status, response = validators.check_exchange_info("binance")
        assert valid_request == True
        assert status == None
        assert response['exchange-object'] is not None

    def test_invalid_input(self):
        valid_request, status, response = validators.check_exchange_info("random")
        assert valid_request == False
        assert status == 400
        assert response['error'] == 'exchange_error'


class Test_check_historical_data(object):
    """ Test for the check_historical_data() function with proper, improper, and empty params. """

    def test_proper_input(self):
        """ Checking proper input returns true. """
        data = {
            'exchange': 'binance',
            'symbol': 'ETH/BTC',
            'timeframe': '1m',
            'start': '2018-01-01 00:00:00',
            'end': '2018-05-01 00:00:00'
        }
        valid_request, status, response = validators.check_historical_data(data)
        assert valid_request == True
        assert status == None
        assert response is not None

    def test_empty_input(self):
        """ Checking empty input returns false and proper return. """
        data = {}
        valid_request, status, response = validators.check_historical_data(data)
        assert valid_request == False
        assert status == 400
        assert response['error'] == 'invalid_request'

    def test_partial_data(self):
        """ Checking partial data returns false and proper return. """
        data = {
            'exchange': 'binance',
        }
        valid_request, status, response = validators.check_historical_data(data)
        assert valid_request == False
        assert status == 400
        assert response['error'] == 'invalid_request'

    def test_unknown_exchange(self):
        """ Checking if exchange name is unknown, it returns proper error. """
        data = {
            'exchange': 'random_unknown_name',
            'symbol': 'ETH/BTC',
            'timeframe': '1m',
            'start': '2018-01-01 00:00:00',
            'end': '2018-05-01 00:00:00'
        }
        valid_request, status, response = validators.check_historical_data(data)
        assert valid_request == False
        assert status == 400
        assert response['error'] == 'exchange_error'

    def test_exchange_support_for_historical_data(self):
        """ Checking if valid exchange has support for historical data. """
        data = {
            'exchange': 'coinmarketcap',
            'symbol': 'ETH/BTC',
            'timeframe': '1m',
            'start': '2018-01-01 00:00:00',
            'end': '2018-05-01 00:00:00'
        }
        valid_request, status, response = validators.check_historical_data(data)
        assert valid_request == False
        assert status == 400
        assert response['error'] == 'historical_error'

    def test_exchange_support_for_timeframe(self):
        """ Checking if valid exchange has support for the given timeframe. """
        data = {
            'exchange': 'binance',
            'symbol': 'ETH/BTC',
            'timeframe': '2m',
            'start': '2018-01-01 00:00:00',
            'end': '2018-05-01 00:00:00'
        }
        valid_request, status, response = validators.check_historical_data(data)
        assert valid_request == False
        assert status == 400
        assert response['error'] == 'timeframe_error'

    def test_exchange_support_for_symbol(self):
        """ Checking if valid exchange has support for the given symbol. """
        data = {
            'exchange': 'binance',
            'symbol': 'ETH/USD',
            'timeframe': '1m',
            'start': '2018-01-01 00:00:00',
            'end': '2018-05-01 00:00:00'
        }
        valid_request, status, response = validators.check_historical_data(data)
        assert valid_request == False
        assert status == 400
        assert response['error'] == 'symbol_error'
