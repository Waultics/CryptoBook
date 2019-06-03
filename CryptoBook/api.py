from utils import get_ip, exchange_info, historical_data
from validators import check_historical_data

from sanic.response import json
from sanic import Sanic
import yaml
import os

app = Sanic()

@app.route('/api/v1/cryptobook/ip')
async def api_get_ip(request):
    """ Returns the public IP address of the API server. """
    return json(await get_ip())

@app.route('/api/v1/cryptobook/exchange/<exchange_name:[A-z]+>')
async def api_exchange_info(request, exchange_name):
    """ Returns information about the exchange. """
    return json(await exchange_info(exchange = exchange_name), status=200)

@app.route('/api/v1/cryptobook/historical', methods=["POST"])
async def api_historical_data(request):
    """ Returns historical exchange data. """

    valid_request, response = check_historical_data(request.json)
    if not valid_request:
        return response
    else:
        return json(await historical_data(exchange=request.json['exchange'],
                                          symbol=request.json['symbol'],
                                          timeframe=request.json['timeframe'],
                                          start=request.json['start'],
                                          end=request.json['end'],
                                          exchange_object = response['exchange-object']),
                                          status=200)

if __name__ == '__main__':
    file = "../config.yml" if os.path.isfile("../config.yml") else "config.yml"
    with open(file, 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)

    app.run(host=config['host'], port=config['port'])
