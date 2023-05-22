import logging
from base64 import b64decode
from os import getenv
from typing import Tuple, Optional

from psycopg2 import (
    connect,
    connection as ps_connection,
    cursor as ps_cursor,
    extras,
)


class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance
        cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


class Database(metaclass=SingletonMeta):
    __logger = logging.getLogger(__name__)
    __connectinon: Optional[ps_connection] = None
    __cursor: Optional[ps_cursor] = None

    @classmethod
    def create_connection(cls) -> Tuple[ps_connection, ps_cursor]:
        try:
            db_name = getenv("DATABSE_NAME")
            conn = connect(
                host=getenv("DB_HOST"),
                database=db_name,
                user=getenv("DB_USER"),
                password=b64decode(getenv("DB_USER_PASSWD")).decode('utf-8'),
            )
            cur = conn.cursor(cursor_factory=extras.DictCursor)

            cls.__logger.info('Created connection to %s', db_name)
        except Exception as error:
            cls.__logger.critical(error)

        return conn, cur

    @classmethod
    def get_session(cls):
        if cls.__connectinon is None:
            cls.__connectinon, cls.__cursor = cls.create_connection()

        return cls.__connectinon, cls.__cursor

    @classmethod
    def dispose_connection(cls):
        cls.__logger.info('Connection has been disposed')

        cls.__connectinon.close()
        cls.__cursor.close()
        cls.__connectinon = cls.__cursor = None
