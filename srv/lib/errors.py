import psycopg2
import falcon
import logging

logger = logging.getLogger(__name__)

# class to emit errors to web application
class BaseError(Exception):
    def __init__(self, e, message: str='internal server error'):
        super().__init__()
        logger.error('error: ', e)
        self.code = falcon.HTTP_INTERNAL_SERVER_ERROR
        self.message = message

class DBUniqueError(BaseError):
    def __init__(self, error: psycopg2.errors.UniqueViolation):
        print(error)
        super().__init__(error, error.pgerror.split('\n')[1][9:])
        self.code = falcon.HTTP_BAD_REQUEST