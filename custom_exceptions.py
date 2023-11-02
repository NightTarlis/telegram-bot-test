
class BaseAppException(Exception):
    message = 'Base app exception'


class PriceServiceException(BaseAppException):
    message = 'Что-то не так, подробности в логах'
