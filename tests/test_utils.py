from CryptoBook import utils
import pytest

@pytest.mark.asyncio
async def test_get_ip():
    """ Tests to verify that get_ip() function returns a dictionary without error. """
    assert type(await utils.get_ip()) == dict

@pytest.mark.asyncio
async def test_get_exchange_info():
    """ Tests to verify that get_exchange_info() function returns a dictionary without error. """
    assert type(await utils.exchange_info('binance')) == dict

@pytest.mark.asyncio
async def test_get_historical_data():
    """ Tests to verify that get_historical_data() function returns a dictionary without error. """
    call = await utils.historical_data(symbol = 'BTC\ETH', ex = 'binance', timeframe = '5m', start = '2018-01-01 00:00:00', end = '2018-01-01 00:01:00')
    assert type(call) == dict
