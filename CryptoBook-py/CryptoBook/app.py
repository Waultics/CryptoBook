if __name__ == "__main__":  # pragma: no cover
    """ Boot-ups the CryptoBook server."""

    # Importing in here for no coverage.
    from api import app
    import urllib3
    import yaml

    # Removes urlib3 warnings.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # Loads the configuration file.
    with open("config.yml", "r") as ymlfile:
        config = yaml.safe_load(ymlfile)["py"]
    # Boots up Sanic server.
    app.run(host=config["host"], port=config["port"])
