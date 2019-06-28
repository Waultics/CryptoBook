/**

npm install --save-dev mocha chai
npm test
*/
var expect = require('chai').expect;
var CCC = require('../ccc-streamer-utilities.js');

describe('CCC.UTILS.dataUnpackCurrent()', function() {
  it('should unpack CURRENT crypto information', function() {
    // sample CURRENT return message from CCC streaming socket.
    var test_msg =
      '2~Coinbase~BTC~USD~2~11806.72~1561719250~0.00113844~' +
      '13.4412423168~67919414~20052.18849144~226701949.1695892~' +
      '63925.8635911704~712570558.2650563~11159.29~12000~10737.87~' +
      '11675.07~12188.57~10300~1423.230431740001~16845215.4784886~11880.37~' +
      '12000~11681.02~fbffe9';

    var messageSubscription = '2~Coinbase~BTC~USD';
    var test_msg_unpacked = {
      TYPE: '2',
      MARKET: 'Coinbase',
      FROMSYMBOL: 'BTC',
      TOSYMBOL: 'USD',
      FLAGS: '2',
      PRICE: 11806.72,
      LASTUPDATE: 1561719250,
      LASTVOLUME: 0.00113844,
      LASTVOLUMETO: 13.4412423168,
      LASTTRADEID: 67919414,
      VOLUMEHOUR: 20052.18849144,
      VOLUMEHOURTO: 226701949.1695892,
      VOLUME24HOUR: 63925.8635911704,
      VOLUME24HOURTO: 712570558.2650563,
      OPENHOUR: 11159.29,
      HIGHHOUR: 12000,
      LOWHOUR: 10737.87,
      OPEN24HOUR: 11675.07,
      HIGH24HOUR: 12188.57,
      LOW24HOUR: 10300
    };
    ccc_msg_unpacked = {}
    var ccc_msg_unpacked = CCC.UTILS.dataUnpackCurrent(
      test_msg,
      ccc_msg_unpacked);
    expect(ccc_msg_unpacked.hasOwnProperty(
      messageSubscription)).to.equal(true);
    expect(test_msg_unpacked).to.eql(
      ccc_msg_unpacked[messageSubscription]);
  });
});

describe('CCC.UTILS.dataUnpack()', function() {
  it('should unpack CURRENTAGG crypto information, which' +
    ' is normally composed of a volume message and a price' +
    ' message',
    function() {
      // sample CURRENT return message from CCC streaming socket.

      var messageSubscription = '5~CCCAGG~BTC~USD';

      var test_msg_1 =
        '5~CCCAGG~BTC~USD~4~11773.15~1561726053~0.006~70.782~372817448~' +
        '71398.82423056324~815703872.9191962~184458.1409871855~' +
        '2062406366.1168025~11154.04~12098.15~10772.75~11723.1~12108.85~' +
        '10323.24~Bitfinex~4943.858955769872~58507966.43108087~12081.11~' +
        '12089.06~11717.98~181915.96137693452~2033890459.9661674~3ffffe9';
      var test_msg_2 =
        '5~CCCAGG~BTC~USD~2~11773.1~71399.38375839325~815710447.7684635~' +
        '184458.70051501552~2062412940.9660697~11723.09~12108.84~' +
        '4944.418483599872~58514541.28034813~198f01';

      var test_msg_unpacked_1 = {
        TYPE: '5',
        MARKET: 'CCCAGG',
        FROMSYMBOL: 'BTC',
        TOSYMBOL: 'USD',
        FLAGS: '4',
        PRICE: 11773.15,
        LASTUPDATE: 1561726053,
        LASTVOLUME: 0.006,
        LASTVOLUMETO: 70.782,
        LASTTRADEID: '372817448',
        VOLUMEHOUR: 71398.82423056324,
        VOLUMEHOURTO: 815703872.9191962,
        VOLUME24HOUR: 184458.1409871855,
        VOLUME24HOURTO: 2062406366.1168025,
        OPENHOUR: 11154.04,
        HIGHHOUR: 12098.15,
        LOWHOUR: 10772.75,
        OPEN24HOUR: 11723.1,
        HIGH24HOUR: 12108.85,
        LOW24HOUR: 10323.24,
        LASTMARKET: 'Bitfinex',
        CHANGE24HOUR: '$ 50.05',
        CHANGE24HOURPCT: '0.43%'
      };
      var test_msg_unpacked_2 = {
        TYPE: '5',
        MARKET: 'CCCAGG',
        FROMSYMBOL: 'BTC',
        TOSYMBOL: 'USD',
        FLAGS: '2',
        PRICE: 11773.1,
        LASTUPDATE: 1561726053,
        LASTVOLUME: 0.006,
        LASTVOLUMETO: 70.782,
        LASTTRADEID: '372817448',
        VOLUMEHOUR: 71399.38375839325,
        VOLUMEHOURTO: 815710447.7684635,
        VOLUME24HOUR: 184458.70051501552,
        VOLUME24HOURTO: 2062412940.9660697,
        OPENHOUR: 11154.04,
        HIGHHOUR: 12098.15,
        LOWHOUR: 10772.75,
        OPEN24HOUR: 11723.09,
        HIGH24HOUR: 12108.84,
        LOW24HOUR: 10323.24,
        LASTMARKET: 'Bitfinex',
        CHANGE24HOUR: '$ 50.01',
        CHANGE24HOURPCT: '0.43%'
      };

      ccc_msg_unpacked = {}
      // First msg.
      ccc_msg_unpacked = CCC.UTILS.dataUnpack(test_msg_1,
        ccc_msg_unpacked);
      expect(ccc_msg_unpacked.hasOwnProperty(
        messageSubscription)).to.equal(true);
      expect(test_msg_unpacked_1).to.eql(
        ccc_msg_unpacked[messageSubscription]);
      // Second msg.
      ccc_msg_unpacked = CCC.UTILS.dataUnpack(test_msg_2,
        ccc_msg_unpacked);
      expect(ccc_msg_unpacked.hasOwnProperty(
        messageSubscription)).to.equal(true);
      expect(test_msg_unpacked_2).to.eql(
        ccc_msg_unpacked[messageSubscription]);
    });
});

describe('CCC.UTILS.dataUnpackTrade()', function() {
  it('should unpack TRADE crypto information', function() {
    // sample CURRENT return message from CCC streaming socket.
    var test_msg =
      '0~Coinbase~BTC~USD~1~67933426~1561727031~' +
      '0.04452259~11715~521.58214185~1561727032~3f';

    var messageSubscription = '0~Coinbase~BTC~USD';
    var test_msg_unpacked =
      { T: '0',
        M: 'Coinbase',
        FSYM: 'BTC',
        TSYM: 'USD',
        F: '1',
        ID: '67933426',
        TS: '1561727031',
        Q: '0.04452259',
        P: '11715',
        TOTAL: '521.58214185' };

    ccc_msg_unpacked = {}
    var ccc_msg_unpacked = CCC.UTILS.dataUnpackTrade(
      test_msg,
      ccc_msg_unpacked);
    expect(ccc_msg_unpacked.hasOwnProperty(
      messageSubscription)).to.equal(true);
    expect(test_msg_unpacked).to.eql(
      ccc_msg_unpacked[messageSubscription]);
  });
});
