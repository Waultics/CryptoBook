from utils import get_ip, exchange_info, historical_data
from validators import check_exchange_info, check_historical_data

from sanic.response import json
from sanic import Sanic
import asyncio
import yaml
import os

app = Sanic()

def load_config():
    """ Loads the config file and runs the Sanic app. """
    with open("config.yml", 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)

    return config['host'], config['port']

@app.route('/api/v1/cryptobook/ip')
async def api_get_ip(request):
    """ Returns the public IP address of the API server. """
    return json(await get_ip())

@app.route('/api/v1/cryptobook/exchange/<exchange_name:[A-z]+>')
async def api_exchange_info(request, exchange_name):
    """ Returns information about the exchange. """
    valid_request, status, response = await check_exchange_info(exchange_name)
    if not valid_request:
        return json(response, status=status)
    else:
        return json(await exchange_info(exchange = exchange_name), status=200)

@app.route('/api/v1/cryptobook/historical', methods=["POST"])
async def api_historical_data(request):
    """ Returns historical exchange data. """

    valid_request, status, response = await check_historical_data(request.json)
    if not valid_request:
        return json(response, status=status)
    else:
        req = {
            'exchange':request.json['exchange'],
            'symbol':request.json['symbol'],
            'timeframe':request.json['timeframe'],
            'start':request.json['start'],
            'end':request.json['end']
        }

        if 'cfbypass' in request.json:
            return json(await historical_data(**req, cfbypass=request.json['cfbypass']), status=200)
        else:
            return json(await historical_data(**req), status=200)

# 'pragma' line below insures Coverall does not bother checking this function for coverage.
if __name__ == '__main__': # pragma: no cover
    host, port = load_config()
    app.run(host=host, port=port)
