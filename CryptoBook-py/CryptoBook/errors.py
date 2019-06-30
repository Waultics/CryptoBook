class HistoricalData(BaseException):
    """ General error for the historical data method in utils. """


class ExchangeDataAccuracyError(HistoricalData):
    """ The exchange responded with innacurate data than those originally requested. """


class NetworkError(HistoricalData):
    """ Unable to properly load the resource due to network error. """
