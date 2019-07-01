from handlers import ip, exchange_info, historical_data

from sanic.response import json
from sanic import Sanic

app = Sanic()


@app.route("/api/v1/cryptobook/ip")
async def api_ip(request):
    """ Returns the public IP address of the API server. """
    response, status = await ip()
    return json(body=response, status=status)


@app.route("/api/v1/cryptobook/exchange/<exchange:[A-z]+>")
async def api_exchange_info(request, exchange):
    """ Returns information about the exchange. """
    response, status = await exchange_info(exchange)
    return json(body=response, status=status)


@app.route("/api/v1/cryptobook/historical", methods=["POST"])
async def api_historical_data(request):
    """ Returns historical exchange data. """
    response, status = await historical_data(request.json)
    return json(body=response, status=status)
