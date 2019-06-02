from CryptoBook import validators

def test_check_historical_data():
    """ Test for the check_historical_data() function with proper, improper, and empty params. """

    test_request = {
        'symbol': 'string',
        'exchange': 'string',
        'timeframe': 'string',
        'start': '2018-01-01 00:00:00',
        'end': '2018-01-01 00:00:00'
    }
    assert validators.check_historical_data(test_request)[0] == True

    test_request = {
        'symbol': 10,
        'exchage': 'string',
        'timeframe': 'string',
        'start': '2018-01-01 00:00:00',
        'end': '2018-01-01 00:00:00'
    }
    assert validators.check_historical_data(test_request)[0] == False

    test_request = ""
    assert validators.check_historical_data(test_request)[0] == False
