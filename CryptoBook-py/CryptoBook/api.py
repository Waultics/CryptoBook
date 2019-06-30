from handlers import ip, exchange_info, historical_data

from sanic.response import json
from sanic import Sanic
import urllib3
import yaml

app = Sanic()


def load_config():
    """ Loads the config file and runs the Sanic app. """
    with open("config.yml", "r") as ymlfile:
        config = yaml.safe_load(ymlfile)

    return config["py"]["host"], config["py"]["port"]


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


if __name__ == "__main__":  # pragma: no cover
    # Disables urllib3 warnings about SSL certificates.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Loads app config, and runs it.
    host, port = load_config()
    app.run(host=host, port=port)
