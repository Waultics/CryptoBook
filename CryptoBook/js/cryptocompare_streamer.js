// cryptocompare utils
var CCC = require('./ccc-streamer-utilities.js');
// websocket client - `npm install -g socket.io-client`
var io = require('socket.io-client');

var currentPrice = {};
var socket = io.connect('https://streamer.cryptocompare.com/');
//Format: {SubscriptionId}~{ExchangeName}~{FromSymbol}~{ToSymbol}
//Use SubscriptionId 0 for TRADE, 2 for CURRENT, 5 for CURRENTAGG eg use key '5~CCCAGG~BTC~USD' to get aggregated data from the CCCAGG exchange 
//Full Volume Format: 11~{FromSymbol} eg use '11~BTC' to get the full volume of BTC against all coin pairs
//For aggregate quote updates use CCCAGG ags market
//var subscription = ['5~CCCAGG~BTC~USD', '5~CCCAGG~ETH~USD', '11~BTC', '11~ETH'];
var subscription = ['5~CCCAGG~BTC~USD'];
socket.emit('SubAdd', { subs: subscription });
socket.on("m", function(message) {
	//console.log(message);
	var messageType = message.substring(0, message.indexOf("~"));
	if (messageType == CCC.STATIC.TYPE.CURRENTAGG) {
		dataUnpack(message);
	}
	else if (messageType == CCC.STATIC.TYPE.FULLVOLUME) {
		decorateWithFullVolume(message);
	}
});

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
	//displayData(currentPrice[pair], from, tsym, fsym);
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
		
	//displayData(currentPrice[pair], from, tsym, fsym);
};
