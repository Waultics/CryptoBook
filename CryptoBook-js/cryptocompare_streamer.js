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
var io_serv = require('socket.io')(server);

server.listen(config.js.port, config.js.host);

io_serv.on('connection', function(connected_socket) {
  console.log("CONNECTED");
  connected_socket.on('subscribe', function(subscriptions) {
    subscriptions.forEach(function(subscription, index) {
      connected_socket.join(subscription);
    });
    socket.emit('SubAdd', {
      subs: subscriptions
    });
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

  io_serv.sockets.in(messageSubscription).emit('response', returnMsg);
  // io_serv.sockets.emit('response', {market_data: currentPrice});
});
