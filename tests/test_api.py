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


def test_load_config():
    """ Test the load_config() function to ensure that config.yml file gets loaded. """
    host, port = api.load_config()
    assert type(host) == str
    assert type(port) == int


class Test_get_ip(object):
    """ Tests the function api_get_ip_get for response status, and response json. """

    async def test(self, application):
        """ Checks correct response is replied to. """
        resp = await application.get("/api/v1/cryptobook/ip")
        resp_json = await resp.json()
        assert resp.status == 200
        assert resp_json.keys() == set(["ip"])


class Test_exchange_info(object):
    """ Tests the function api_exchange_info for response status, and response json. """

    async def test_proper_input(self, application):
        """ Checks correct response is replied to. """
        resp = await application.get("/api/v1/cryptobook/exchange/binance")
        resp_json = await resp.json()
        assert resp.status == 200
        assert resp_json.keys() == set(
            ["exchange", "symbols", "timeframes", "historical"]
        )

    async def test_inproper_input(self, application):
        """ Checks invalid response is correctly replied to. """
        resp = await application.get("/api/v1/cryptobook/exchange/random")
        resp_json = await resp.json()
        assert resp.status == 400
        assert set(["error", "description"]).issubset(resp_json.keys())


class Test_historical_data(object):
    """ Tests the function api_historical_data for response status, and response json. """

    async def test_proper_input(self, application):
        """ Checks valid response is correctly replied to. """
        data = {
            "exchange": "binance",
            "symbol": "ETH/BTC",
            "timeframe": "1m",
            "start": "2018-01-01 00:00:00",
            "end": "2018-05-01 00:00:00",
        }
        resp = await application.post(
            "/api/v1/cryptobook/historical", data=json.dumps(data)
        )
        resp_json = await resp.json()
        assert resp.status == 200
        assert resp_json.keys() == set(["index", "columns", "data"])

    async def test_proper_input_with_cfbypass(self, application):
        """ Checks valid response is correctly replied to. """
        data = {
            "exchange": "binance",
            "symbol": "ETH/BTC",
            "timeframe": "1m",
            "start": "2018-01-01 00:00:00",
            "end": "2018-05-01 00:00:00",
            "cfbypass": True,
        }
        resp = await application.post(
            "/api/v1/cryptobook/historical", data=json.dumps(data)
        )
        resp_json = await resp.json()
        assert resp.status == 200
        assert resp_json.keys() == set(["index", "columns", "data"])

    async def test_inproper_input(self, application):
        """ Checks invalid response is correctly replied to. """
        data = {}
        resp = await application.post(
            "/api/v1/cryptobook/historical", data=json.dumps(data)
        )
        resp_json = await resp.json()
        assert resp.status == 400
        assert set(["error", "description"]).issubset(resp_json.keys())
