from db.db_exceptions import DbException, DbExceptionReason
from fastapi import HTTPException, status
from functools import wraps
from helpers.functions import contains_explicit_return


class ExceptionsConverter:
    exception: DbException

    def __init__(self, e: DbException):
        super().__init__()
        self.exception = e

    def http(self):
        exc: HTTPException = status.HTTP_500_INTERNAL_SERVER_ERROR
        match self.exception.reason:
            case DbExceptionReason.NOT_FOUND:
                exc = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=self.exception.detail)
            case DbExceptionReason.FORBIDDEN:
                exc = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail=self.exception.detail)
            case DbExceptionReason.ACTION_IMPOSSIBLE:
                exc = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=self.exception.detail)
        return exc


def exceptions_converter(action):
    @wraps(action)
    def wrapper(*args, **kwargs):
        try:
            if contains_explicit_return(action):
                return action(*args, **kwargs)
            else:
                action(*args, **kwargs)
        except DbException as e:
            raise ExceptionsConverter(e).http()
    return wrapper

