from app.db.implementations.database import Database
from app.db.repositories.interfaces.base import IRepository


class Repository(IRepository):
    def __init__(self, databse: Database):
        self._connection, self._cursor = databse.get_connection()
