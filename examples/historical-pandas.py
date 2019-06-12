import pandas as pd
import requests
import json

data = {
    'exchange':'binance',
    'symbol':'ETH/BTC',
    'timeframe':'1m',
    'start':'2018-01-01 00:00:00',
    'end':'2018-01-05 00:00:00',
    'cfbypass': False # Optional flag if exchange uses CloudFlare.
}

# Sends a request to the server with the data provided above.
r = requests.post(url="http://0.0.0.0:9900/api/v1/cryptobook/historical", data=json.dumps(data))

# Reads the request.
df = pd.read_json(r.text, orient='split')

# Converts the Time column to DateTime objects.
df['Time'] = pd.to_datetime(df['Time'], unit='ms')

# Prints the DataFrame.
print(df.to_string())
