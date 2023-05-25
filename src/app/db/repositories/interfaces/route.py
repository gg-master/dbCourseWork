from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import Route


class IRouteRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[Route]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> Route:
        ...

    @abstractmethod
    def add(self, item: Route) -> int:
        ...

    @abstractmethod
    def update(self, item: Route) -> None:
        ...
