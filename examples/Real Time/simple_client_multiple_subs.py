"""
Subscription Format: {SubscriptionId}~{ExchangeName}~{FromSymbol}~{ToSymbol}

SubscriptionId:
    - 0 for TRADE
    - 2 for CURRENT
    - 5 for CURRENTAGG

Examples:
    - ['5~CCCAGG~BTC~USD'] : get aggregated data from the CCCAGG exchange
    - ['0~Kraken~BTC~USD'] : get all BTC/USD trades from Kraken

---
Full Volume Subscription Format: 11~{FromSymbol}
Examples:
    - ['11~BTC'] : get the full volume of BTC against all coin pairs

"""

import socketio
import pprint

pp = pprint.PrettyPrinter(indent=2)

sio = socketio.Client()

@sio.on('response')
def my_event(data):
    pp.pprint(data)

@sio.event
def connect():
    print("CONNECTED")

@sio.event
def disconnect():
    print("DISCONNECTED")


sio.connect('http://0.0.0.0:5050')

subscription = ['5~CCCAGG~BTC~USD', '5~CCCAGG~ETH~USD']
sio.emit('subscribe', subscription)
