CryptoBook
==================

A RESTful API project that allows easy gathering of historical and live cryptocurrency data with ease. To be utilized as a microservice for larger projects.


Features
------------------

* Gather historical data from over 200 cryptocurrency exchanges.
* Gather historical data from CoinMarketCap with ease.

Requirements
------------------

* Python **3.5** or higher.
* `aiohttp <https://pypi.python.org/pypi/aiohttp>`_
* `ccxt <https://github.com/ccxt/ccxt>`_
* `ppyaml <https://github.com/yaml/pyyaml>`_
* `pandas <https://github.com/pandas-dev/pandas>`_
* `cerberus <https://github.com/pyeve/cerberus>`_

Installation
------------------

Latest development version can be installed straight from Github.

.. code-block:: bash

    $ pip install -U git+https://github.com/Waultics/CryptoBook.git
    cd CryptBook
    $ python CryptoBook/api.py

It is recommended, however, to utilize Docker to run CryptoBook.

.. code-block:: bash

    $ docker build -t cryptobook .
    $ docker run -p 9900:9900 -t cryptobook


Using Proxies
--------------

To use proxies with CryptoBook it is recommended to use `Frontman <https://github.com/synchronizing/Frontman>`_, which wraps `ProxyBroker <https://github.com/constverum/ProxyBroker>`_ in a customizable docker container. ProxyBroker allows the creation of a local proxy server that routes internet traffic through filtered and working proxies. You will then have to create a `docker-compose.yml` file to set the `http_proxy` and `https_proxy` environment variables for CryptoBook, and link each container (further instructions in the Frontman repo).


Contributing
------------------

* Fork it: https://github.com/Waultics/CryptoBook/fork
* Create your feature branch: git checkout -b my-new-feature
* Commit your changes: git commit -am 'Add some feature'
* Push to the branch: git push origin my-new-feature
* Submit a pull request!


License
------------------

Licensed under the MIT License.

Contents
==================

.. toctree::

   api
   utils
   validators

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
