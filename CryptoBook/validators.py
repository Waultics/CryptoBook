from cerberus import Validator
from datetime import datetime

def check_historical_data(request):
    """ Verify json request for /api/v1/cryptobook/historical endpoint. """

    v = Validator()
    date = lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    v.schema = {'symbol': {'type': 'string'},
                'exchange': {'type': 'string'},
                'timeframe': {'type': 'string'},
                'start': {'type': 'datetime', 'coerce': date},
                'end': {'type': 'datetime', 'coerce': date}}

    if v.validate(request):
        return True, {}
    else:
        return False, v.errors
