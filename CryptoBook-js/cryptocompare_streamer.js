/**
Format: {SubscriptionId}~{ExchangeName}~{FromSymbol}~{ToSymbol}
Use SubscriptionId 0 for TRADE, 2 for CURRENT, 5 for CURRENTAGG eg use key '5~CCCAGG~BTC~USD' to get aggregated data from the CCCAGG exchange
Full Volume Format: 11~{FromSymbol} eg use '11~BTC' to get the full volume of BTC against all coin pairs
For aggregate quote updates use CCCAGG ags market

Node packages:
  - websocket client. - `npm install -g socket.io-client`
  - Server. - `npm install -g express`
*/

// cryptocompare utils
var CCC = require('./ccc-streamer-utilities.js');

yaml = require('js-yaml');
fs = require('fs');
var config = yaml.safeLoad(fs.readFileSync('config.yml', 'utf8'));
// initialize a client socket to connect to cryptocompare
var io = require('socket.io-client');
var socket = io.connect('https://streamer.cryptocompare.com/');

// this dictionary contains the most up-to-date crypto data
currentPrice = {};

// intialize a server socket to connect to anybody who's interested
var app = require('express')();
var server = require('http').Server(app);
server.listen(config.js.port, config.js.host);
var io_serv = require('socket.io')(server);

io_serv.of(config.js.namespace)
  .on('connection', function(connected_socket) {
  console.log(connected_socket.id + " CONNECTED");
  connected_socket.on('subscribe', function(subscriptions) {
    subscriptions.forEach(function(subscription, index) {
      connected_socket.join(subscription);
    });
    socket.emit('SubAdd', {
      subs: subscriptions
    });
  });
  connected_socket.on('disconnect', function() {
      console.log(connected_socket.id + " DISCONNECTED");
  });
});

// subscribe the client (io) to the cryptocompare ws
// sample sub: var subscription = ['0~Kraken~BTC~USD'];
// each time a message is recieved.
socket.on("m", function(message) {
  var messageType = message.substring(0, message.indexOf("~"));
  var messageSubscription = CCC.UTILS.getSubscriptionFromMessage(message);

  if (messageType == CCC.STATIC.TYPE.CURRENTAGG) {
    currentPrice = CCC.UTILS.dataUnpack(message, currentPrice);
  } else if (messageType == CCC.STATIC.TYPE.FULLVOLUME) {
    currentPrice = CCC.UTILS.decorateWithFullVolume(message, currentPrice);
  } else if (messageType == CCC.STATIC.TYPE.TRADE) {
    currentPrice = CCC.UTILS.dataUnpackTrade(message, currentPrice);
  } else if (messageType == CCC.STATIC.TYPE.CURRENT) {
    currentPrice = CCC.UTILS.dataUnpackCurrent(message, currentPrice);
  }
  unpacked = currentPrice[messageSubscription];

  var returnMsg = {};
  returnMsg[messageSubscription] = unpacked;

  emitToSocketsInRoomAndNamespace(messageSubscription,
                                  config.js.namespace,
                                  'response',
                                  returnMsg);
});

function emitToSocketsInRoomAndNamespace(room_name, namespace, event_name, returnMsg) {
  ns = io_serv.of(namespace || "/");
  if (ns) {
    for (var id in ns.connected) {
      var rooms_of = Object.keys(ns.connected[id].rooms);
      if (rooms_of.includes(room_name)) {
        ns.connected[id].emit(event_name, returnMsg);
      }
    }
  }
}
