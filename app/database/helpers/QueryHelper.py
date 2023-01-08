from functools import wraps
from typing import Callable, Any

from database.connections.DataBaseConnection import DataBaseConnection


class QueryHelper:
    @staticmethod
    def query(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args,
                    **kwargs) -> Any:
            with DataBaseConnection().cursor() as cursor:
                outcome = func(*args, **kwargs, cur=cursor)
                DataBaseConnection().commit()
                return outcome

        return wrapper
