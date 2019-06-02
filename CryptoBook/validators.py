from cerberus import Validator, DocumentError
from datetime import datetime

def check_historical_data(request):
    """ Verify json request for /api/v1/cryptobook/historical endpoint.

    Args:
        request (str): The request sent into the server for verification.

    Returns:
        bool: Boolean representing whether or not check was successfull or failure.
        dict: Errors corresponding to the data validation. Empty if return bool is true.
    """

    v = Validator()
    date = lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    v.schema = {'symbol': {'type': 'string'},
                'exchange': {'type': 'string'},
                'timeframe': {'type': 'string'},
                'start': {'type': 'datetime', 'coerce': date},
                'end': {'type': 'datetime', 'coerce': date}}

    try:
        if v.validate(request):
            return True, {}
        else:
            return False, v.errors
    except DocumentError:
        return False, {'Document is missing.'}
