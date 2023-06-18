from app.db.implementations import PostgresDbConnector
from app.db.repositories.interfaces.base import IRepository


class Repository(IRepository):
    def __init__(self, databse_connector: PostgresDbConnector):
        self._connection, self._cursor = databse_connector.get_connection()
