<p align="center">
  <img width="460" src="./assets/CryptoBook Header.png">
  <br>
  [![Travis](https://travis-ci.com/Waultics/CryptoBook.svg?branch=master)](https://travis-ci.com/Waultics/CryptoBook) [![Coverage Status](https://coveralls.io/repos/github/Waultics/CryptoBook/badge.svg?branch=master)](https://coveralls.io/github/Waultics/CryptoBook?branch=master)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</p>


A RESTful API project that allows easy gathering of historical and live cryptocurrency data with ease. To be utilized as a microservice for larger projects.

---

## Documentation

Documentation can be found at the following link.

---

## Requirements

* Python **3.6** or higher.
* `aiohttp <https://pypi.python.org/pypi/aiohttp>`_
* `ccxt <https://github.com/ccxt/ccxt>`_
* `ppyaml <https://github.com/yaml/pyyaml>`_
* `pandas <https://github.com/pandas-dev/pandas>`_
* `cerberus <https://github.com/pyeve/cerberus>`_


---

## Installation

Latest development version can be installed straight from Github.

```bash
$ pip install -U git+https://github.com/Waultics/CryptoBook.git
cd CryptoBook
$ python CryptoBook/api.py
```

It is recommended, however, to utilize Docker to run CryptoBook.

```bash
$ docker build -t cryptobook .
$ docker run -p 9900:9900 -t cryptobook
```

---

## Using Proxies

To use proxies with CryptoBook it is recommended to use [Frontman](https://github.com/synchronizing/Frontman), which wraps [ProxyBroker](https://github.com/constverum/ProxyBroker) in a customizable docker container. ProxyBroker allows the creation of a local proxy server that routes internet traffic through filtered and working proxies. You will then have to create a `docker-compose.yml` file to set the `http_proxy` and `https_proxy` environment variables for CryptoBook, and link each container (further instructions in the Frontman repo).

---

## Contributing

* Fork it: https://github.com/Waultics/CryptoBook/fork
* Create your feature branch: git checkout -b my-new-feature
* Commit your changes: git commit -am 'Add some feature'
* Push to the branch: git push origin my-new-feature
* Submit a pull request!

---

## License

Licensed under the MIT License.
