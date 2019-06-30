from datetime import datetime
import pandas as pd
import requests
import json

data = {
    "exchange": "binance",
    "symbol": "ETH/BTC",
    "timeframe": "1h",
    "start": "2018-01-01 00:00:00",
    "end": "2018-01-02 00:00:00",
    "cfbypass": True,  # Optional flag if exchange uses CloudFlare.
}
request_before = datetime.now()

# Sends a request to the server with the data provided above.
r = requests.post(
    url="http://0.0.0.0:9900/api/v1/cryptobook/historical", data=json.dumps(data)
)

try:
    request_after = datetime.now()
    dataframe_before = datetime.now()

    # Reads the request.
    df = pd.read_json(r.text, orient="split")
    # Converts the Time column to DateTime objects.
    df["Time"] = pd.to_datetime(df["Time"], unit="ms")

    dataframe_after = datetime.now()

    # Prints the DataFrame.
    print(df.to_string())

    # Printing time resource.
    print("Request time: ", (request_after - request_before).total_seconds())
    print("Dataframe time: ", (dataframe_after - dataframe_before).total_seconds())
except Exception:
    print(r.text)
