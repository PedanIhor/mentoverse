from db.db_exceptions import DbException, DbExceptionReason
from fastapi import HTTPException, status


class ExceptionsConverter:

    def db_to_http(self, e: DbException):
        match e.reason:
            case DbExceptionReason.NOT_FOUND:
                return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
            case DbExceptionReason.FORBIDDEN:
                return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.detail)
