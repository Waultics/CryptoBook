from CryptoBook import api
import pytest
import json

@pytest.yield_fixture
def app():
    """ Creates yield function with our app object. """
    app = api.app()
    yield app

@pytest.fixture
def application(loop, app, sanic_client):
    """ Creates our testing Sanic application. """
    return loop.run_until_complete(sanic_client(app))

async def test_api_get_ip_get(application):
    """ Tests the function api_get_ip_get for response status, and response json. """

    resp = await application.get('/api/v1/cryptobook/ip')
    assert resp.status == 200

    resp_json = await resp.json()
    assert resp_json.keys() == set(['ip'])

async def test_api_exchange_info_get(application):
    """ Tests the function api_exchange_info for response status, and response json. """

    resp = await application.get('/api/v1/cryptobook/exchange/binance')
    assert resp.status == 200

    resp_json = await resp.json()
    assert resp_json.keys() == set(['exchange', 'symbols', 'timeframes', 'historical'])

async def test_api_historical_data_post(application):
    """ Tests the function api_historical_data for response status, and response json. """

    data = {
        'exchange': 'binance',
        'symbol': 'ETH/BTC',
        'timeframe': '1m',
        'start': '2018-01-01 00:00:00',
        'end': '2018-05-01 00:00:00'
    }

    resp = await application.post('/api/v1/cryptobook/historical', data = json.dumps(data))
    assert resp.status == 200

    resp_json = await resp.json()
    assert resp_json.keys() == set(['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
