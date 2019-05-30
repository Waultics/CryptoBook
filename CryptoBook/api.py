from debug import get_ip
from scrapers import scraper_historical_data
from sanic.response import json
from sanic import Sanic
import yaml
import os

app = Sanic()

@app.route('/api/v1/cryptobook/debug/ip')
async def test(request):
    """ Returns the public IP address of the API server. """
    return json(await get_ip())

@app.route('/api/v1/cryptobook/historical', methods=["POST"])
async def historical(request):
    return json(await scraper_historical_data(symbol=request.json['symbol'],
                                              ex=request.json['exchange'],
                                              timeframe=request.json['timeframe'],
                                              start=request.json['start'],
                                              end=request.json['end']))

if __name__ == '__main__':
    file = "../config.yml" if os.path.isfile("../config.yml") else "config.yml"
    with open(file, 'r') as ymlfile:
        config = yaml.safe_load(ymlfile)

    app.run(host=config['host'], port=config['port'])
