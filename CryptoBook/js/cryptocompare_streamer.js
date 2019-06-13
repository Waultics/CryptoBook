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

// this dictionary contains the most up-to-date crypto data
var currentPrice = {};

// initialize a client socket to connect to cryptocompare
var io = require('socket.io-client');
var socket = io.connect('https://streamer.cryptocompare.com/');

// intialize a server socket to connect to anybody who's interested
var app = require('express')();
var server = require('http').Server(app);
const io_serv = require('socket.io')(server);

server.listen(80);

io_serv.on('connection', function(connected_socket){
  console.log("CONNECTED");
  connected_socket.on('subscribe', function(subscription) {
    socket.emit('SubAdd', { subs: subscription });
    console.log(subscription);
  });
});

// subscribe the client (io) to the cryptocompare ws
// sample sub: var subscription = ['0~Kraken~BTC~USD'];
// each time a message is recieved.
socket.on("m", function(message) {
  var messageType = message.substring(0, message.indexOf("~"));

  if (messageType == CCC.STATIC.TYPE.CURRENTAGG) {
    dataUnpack(message);
  } else if (messageType == CCC.STATIC.TYPE.FULLVOLUME) {
    decorateWithFullVolume(message);
  } else if (messageType == CCC.STATIC.TYPE.TRADE) {
    dataUnpackTrade(message);
  }
  io_serv.sockets.emit('response', {market_data: currentPrice});	 
});

var dataUnpackTrade = function(message) {
  var data = CCC.TRADE.unpack(message);
	
  var from = data['FSYM'];
  var to = data['TSYM'];

  var fsym = CCC.STATIC.CURRENCY.getSymbol(from);
  var tsym = CCC.STATIC.CURRENCY.getSymbol(to);
	
  var pair = from + to;
        
  if (!currentPrice.hasOwnProperty(pair)) {
    currentPrice[pair] = {};
  }

  for (var key in data) {
    currentPrice[pair][key] = data[key];
  }
}

// unpack data message into dictionary
var dataUnpack = function(message) {
  var data = CCC.CURRENT.unpack(message);

  var from = data['FROMSYMBOL'];
  var to = data['TOSYMBOL'];
  var fsym = CCC.STATIC.CURRENCY.getSymbol(from);
  var tsym = CCC.STATIC.CURRENCY.getSymbol(to);
  var pair = from + to;

  if (!currentPrice.hasOwnProperty(pair)) {
    currentPrice[pair] = {};
  }

  for (var key in data) {
    currentPrice[pair][key] = data[key];
  }

  if (currentPrice[pair]['LASTTRADEID']) {
    currentPrice[pair]['LASTTRADEID'] = parseInt(currentPrice[pair]['LASTTRADEID']).toFixed(0);
  }
  currentPrice[pair]['CHANGE24HOUR'] = CCC.convertValueToDisplay(tsym, (currentPrice[pair]['PRICE'] - currentPrice[pair]['OPEN24HOUR']));
  currentPrice[pair]['CHANGE24HOURPCT'] = ((currentPrice[pair]['PRICE'] - currentPrice[pair]['OPEN24HOUR']) / currentPrice[pair]['OPEN24HOUR'] * 100).toFixed(2) + "%";
  console.log(currentPrice);
};

// unpack volume message into dictionary
var decorateWithFullVolume = function(message) {
  var volData = CCC.FULLVOLUME.unpack(message);
  var from = volData['SYMBOL'];
  var to = 'USD';
  var fsym = CCC.STATIC.CURRENCY.getSymbol(from);
  var tsym = CCC.STATIC.CURRENCY.getSymbol(to);
  var pair = from + to;

  if (!currentPrice.hasOwnProperty(pair)) {
    currentPrice[pair] = {};
  }

  currentPrice[pair]['FULLVOLUMEFROM'] = parseFloat(volData['FULLVOLUME']);
  currentPrice[pair]['FULLVOLUMETO'] = ((currentPrice[pair]['FULLVOLUMEFROM'] - currentPrice[pair]['VOLUME24HOUR']) * currentPrice[pair]['PRICE']) + currentPrice[pair]['VOLUME24HOURTO'];
  console.log(currentPrice);		
};
