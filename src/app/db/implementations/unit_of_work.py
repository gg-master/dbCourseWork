import logging
import traceback as tb
from app.db.implementations.db_connector import PostgresDbConnector
from app.db.interfaces.unit_of_work import IUnitOfWork


# TODO change this to an adequate implementation
class UnitOfWork(IUnitOfWork):
    __logger = logging.getLogger(__name__)

    def __init__(self, database: PostgresDbConnector) -> None:
        self.__connection = database.get_connection()[0]

    def commit(self):
        self.__connection.commit()

    def rollback(self):
        self.__connection.rollback()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback):
        if ex_type is None:
            self.commit()
        else:
            self.__logger.critical(
                "%s\n%s\n%s: %s",
                ex_value,
                '\n'.join(tb.format_tb(ex_traceback)),
                ex_type.__name__,
                ex_value,
            )
            self.rollback()
        return True
