from db.db_exceptions import DbException
from helpers.exceptions_converter import ExceptionsConverter

def try_db_action(action):
    try:
        return action()
    except DbException as e:
        raise ExceptionsConverter().db_to_http(e)