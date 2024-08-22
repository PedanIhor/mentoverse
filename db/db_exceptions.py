from enum import Enum


class DbExceptionReason(Enum):
    NOT_FOUND = 1
    FORBIDDEN = 2
    VALIDATION = 3
    INTEGRITY = 4


class DbException(Exception):
    def __init__(self, reason: DbExceptionReason, detail: str):
        super().__init__({"detail": detail})
        self.reason = reason
        self.detail = detail
