import os
import sqlite3
import psycopg2
import mysql.connector
from pathlib import Path
from abc import abstractmethod
from dotenv import load_dotenv


load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / '.env')


class SingletonConnector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(SingletonConnector, cls).__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs) -> None:
        self.params = kwargs
        self.__connection = None
        self.__cursor = None
        self.__response = None

    @abstractmethod
    def connect(self):
        ...

    def __execute(self, query: str, data: tuple = None, fetch: bool = False, commit: bool = False) -> None | str:
        try:
            self.__connection = self.connect()
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(query, data) if data else self.__cursor.execute(query)
        except (sqlite3.Error, psycopg2.Error, mysql.connector.Error, Exception) as error:
            return f'{self.__class__.__name__} ERROR_1: {error}'
        else:
            if fetch:
                self.__response = self.__cursor.fetchall()
            if commit:
                self.__connection.commit()
            return self.__response
        finally:
            try:
                self.__cursor.close()
                self.__connection.close()
            except (sqlite3.Error, psycopg2.Error, mysql.connector.Error, Exception) as error:
                return f'{self.__class__.__name__} ERROR_2: {error}'

    def create(self, query: str) -> None:
        return self.__execute(query, commit=True)

    def save(self, query: str, data: tuple) -> None | tuple:
        return self.__execute(query, data, commit=True, fetch=True)

    def fetchall(self, query: str) -> None | tuple:
        return self.__execute(query, fetch=True)

    def fetchone(self, query: str, data: tuple) -> None | tuple:
        return self.__execute(query, data, fetch=True)


class SQLiteConnector(SingletonConnector):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not kwargs:
            self.params = dict(database=f'{os.getenv("DATABASE")}.sqlite3')

    def connect(self):
        return sqlite3.connect(**self.params)

class PostgreSQLConnector(SingletonConnector):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not kwargs:
            self.params = dict(
                database=os.getenv("DATABASE"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
            )

    def connect(self):
        return psycopg2.connect(**self.params)


class MySQLConnector(SingletonConnector):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not kwargs:
            self.params = dict(
                database=os.getenv("DATABASE"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
            )

    def connect(self):
        return mysql.connector.connect(**self.params)