import requests


# Sends a request to the server with the data provided above.
r = requests.get(url="http://0.0.0.0:9900/api/v1/cryptobook/exchange/binance")

# Prints the DataFrame.
print(r.text)
