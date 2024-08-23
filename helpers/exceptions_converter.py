from db.db_exceptions import DbException, DbExceptionReason
from fastapi import HTTPException, status


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
