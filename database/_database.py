from typing import Literal
from ._connectors import SQLiteConnector, MySQLConnector, PostgreSQLConnector


class Database:
    __instance = None

    def __new__(cls, __driver: Literal['postgres', 'mysql', 'sqlite'], *args, **kwargs):
        if not cls.__instance:
            match __driver:
                case 'postgres':
                    cls.__instance = PostgreSQLConnector(*args, **kwargs)
                case 'mysql':
                    cls.__instance = MySQLConnector(*args, **kwargs)
                case 'sqlite':
                    cls.__instance = SQLiteConnector(*args, **kwargs)
                case _:
                    return f'{cls.__name__} 001: Database connection not defined.'
        return cls.__instance
