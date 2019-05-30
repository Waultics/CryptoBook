from debug import get_ip
from scrapers import exchange_info, historical_data
from sanic.response import json
from sanic import Sanic
import yaml
import os

app = Sanic()

@app.route('/api/v1/cryptobook/debug/ip')
async def api_test(request):
    """ Returns the public IP address of the API server. """
    return json(await get_ip())

@app.route('/api/v1/cryptobook/exchange/<exchange_name:[A-z]+>')
async def api_exchange_info(request, exchange_name):
    """ Returns information about the exchange. """
    return json(await exchange_info(exchange_name))

@app.route('/api/v1/cryptobook/historical', methods=["POST"])
async def api_historical_data(request):
    return json(await historical_data(symbol=request.json['symbol'],
                                              ex=request.json['exchange'],
                                              timeframe=request.json['timeframe'],
                                              start=request.json['start'],
                                              end=request.json['end']))

if __name__ == '__main__':
    file = "../config.yml" if os.path.isfile("../config.yml") else "config.yml"
    with open(file, 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)

    app.run(host=config['host'], port=config['port'])
