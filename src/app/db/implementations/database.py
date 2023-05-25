import logging
from base64 import b64decode
from os import getenv
from typing import Tuple, Optional

from psycopg2 import connect, extras, OperationalError
from psycopg2._psycopg import connection as ps_connection, cursor as ps_cursor
from psycopg2.extensions import (
    ISOLATION_LEVEL_AUTOCOMMIT,
    ISOLATION_LEVEL_DEFAULT,
)
from app.db.interfaces.database import IDatabase

from app.misc.utils import get_rsc_path


class Database(IDatabase):
    __logger = logging.getLogger(__name__)
    __connection: Optional[ps_connection] = None
    __cursor: Optional[ps_cursor] = None

    @classmethod
    def get_connection(cls) -> Tuple[ps_connection, ps_cursor]:
        if cls.__connection is not None:
            return cls.__connection, cls.__cursor
        return cls._create_connection()

    @classmethod
    def _create_connection(cls) -> Tuple[ps_connection, ps_cursor]:
        db_name = getenv("DATABASE_NAME")
        host = getenv("DB_HOST")
        user, password = getenv("DB_USER"), getenv("DB_USER_PASSWD")
        try:
            cls.__connection = connect(
                host=host,
                database=db_name,
                user=user,
                password=b64decode(password).decode('utf-8'),
            )
            cls.__cursor = cls.__connection.cursor(
                cursor_factory=extras.DictCursor
            )
            cls.__init_db()

            cls.__logger.info('Created connection to %s db', db_name)
            return cls.__connection, cls.__cursor
        except OperationalError as error:
            cls.__connection = connect(
                user=user,
                password=b64decode(password).decode('utf-8'),
                host=host,
            )
            cls.__cursor = cls.__connection.cursor()

            if not cls.__create_database():
                cls.__logger.critical(error)
                raise error

            cls.dispose_connection()
            cls._create_connection()
        except Exception as error:
            cls.__logger.critical(error)
            raise error

    @classmethod
    def dispose_connection(cls) -> None:
        if cls.__connection is not None:
            cls.__logger.info('Connection to db has been disposed')

            cls.__connection.close()
            cls.__cursor.close()
            cls.__connection = cls.__cursor = None

    @classmethod
    def __create_database(cls) -> bool:
        query = (
            f"SELECT datname FROM pg_database "
            f"WHERE datname = '{getenv('DATABASE_NAME')}'"
        )
        cls.__cursor.execute(query)
        if cls.__cursor.fetchone():
            return False

        cls.__connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        sql_create_database = f'CREATE DATABASE {getenv("DATABASE_NAME")};'
        cls.__cursor.execute(sql_create_database)
        cls.__connection.set_isolation_level(ISOLATION_LEVEL_DEFAULT)
        return True

    @classmethod
    def __init_db(cls):
        if cls.__connection is None:
            return None

        with open(
            get_rsc_path('db/queries/creating_db.sql'), encoding='utf-8'
        ) as file:
            init_query = ''.join(file.readlines())
            cls.__cursor.execute(init_query)
            cls.__connection.commit()
