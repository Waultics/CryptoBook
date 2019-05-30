# 📚 CryptoBook

A small RESTful API build on top of [`Sanic`](https://github.com/huge-success/sanic) that utilizes [`CryptoCurrency eXchange Trading Library (ccxt)`](https://github.com/ccxt/ccxt) and [`CoinMarketCap Historical Data Retrieval (cmc)`](https://github.com/Alescontrela/coinmarketcap-history/) to serve historical market information.

---

## API

CryptoBook offers the following endpoints:

### Debug

#### `/api/v1/cryptobook/debug/ip`
##### `GET`
* Returns the external IP of the server. Good for proxy setting tests.

### Exchange Information

#### `/api/v1/cryptobook/exchange/<exchange_name:[A-z]+>`
##### `GET`
* Returns information about the given market.
* **Returns**
    * `exchange`: Exchange name inputted.
    * `historical`: Whether or not the exchange offers historical data via public API.
    * `symbol`: Valid symbols for this exchange.
    * `timeframe`: Valid timeframes for this exchange.


### Scrapers

#### `/api/v1/cryptobook/historical`
##### `POST`
* **Input**
    * `symbol`: Symbol being looked for (i.e. `BTC\ETH`)
    * `exchange`: Exchange to retrieve historical data from. (i.e. `binance`)
        * Use `id` posted in the `ccxt` documentation, [here](https://github.com/ccxt/ccxt#supported-cryptocurrency-exchange-markets).
    * `timeframe`: Interval of the data. (i.e. `1m`)
    * `start`: Start date to retrieve data from. (i.e. `2018-01-01 00:00:00`)
    * `end`: End date of the retrieval period. (i.e. `2018-05-01 00:00:00`)
* **Returns**
    * Historical market information in `json` format ready to be turned back into a Pandas' `DataFrame` object ([`pd.read_json()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html)).

---

## Building the API Server

The recommended method of starting this server is by utilizing Docker. Simply do the following:

```
docker build -t cryptobook .
docker run -p 9900:9900 -t cryptobook
```

---

## Using Proxies with CryptoBook

To use proxies with CryptoBook it is recommended to use [Frontman](https://github.com/synchronizing/Frontman), which wraps [ProxyBroker](https://github.com/constverum/ProxyBroker) in a customizable docker container. ProxyBroker allows the creation of a local proxy server that routes internet traffic through filtered and working proxies. You will then have to create a `docker-compose.yml` file to set the `http_proxy` and `https_proxy` environment variables for CryptoBook, and link each container (further instructions in the Frontman repo).

---

## To-Do

- [ ] Add the `cmc` library after PyPi update.
- [x] Create `GET` methods for exchange information like `symbol` and `timeframe`.
- [x] Expand on the error throwing checks for `start` and `end` inside the `scraper_historical_data()`.
