from db.db_exceptions import DbException, DbExceptionReason
from fastapi import HTTPException, status


class ExceptionsConverter:
    exception: DbException

    def __init__(self, e: DbException):
        super().__init__()
        self.exception = e

    def http(self):
        match self.exception.reason:
            case DbExceptionReason.NOT_FOUND:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                     detail=self.exception.detail)
            case DbExceptionReason.FORBIDDEN:
                return HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                     detail=self.exception.detail)
            case DbExceptionReason.INTEGRITY:
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                     detail=self.exception.detail)
