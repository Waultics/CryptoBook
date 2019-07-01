class CryptoBookError(BaseException):
    """ General error for Cryptobook. """


class ExchangeDataAccuracyError(CryptoBookError):
    """ The exchange responded with innacurate data than those originally requested. """


class NetworkError(CryptoBookError):
    """ Unable to properly load the resource due to network error. """
