import logging
from typing import List
from app.db.entities import Route
from app.db.repositories.interfaces import IRouteRepository
from app.db.implementations import UnitOfWork, PostgresDbConnector


class RouteService:
    def __init__(self, route_repo: IRouteRepository) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__route_repo = route_repo

    def get(self, item_id: int) -> Route:
        return self.__route_repo.get(item_id)

    def get_all(self) -> List[Route]:
        return self.__route_repo.get_all()

    def create(self, item: Route) -> None:
        with UnitOfWork(PostgresDbConnector):
            self.__route_repo.create(item)

    def update(self, item: Route) -> None:
        with UnitOfWork(PostgresDbConnector):
            self.__route_repo.update(item)

    def delete(self, item_id: int) -> None:
        with UnitOfWork(PostgresDbConnector):
            self.__route_repo.delete(item_id)
