from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import Transport


class ITransportRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[Transport]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> Transport:
        ...

    @abstractmethod
    def add(self, item: Transport) -> int:
        ...

    @abstractmethod
    def update(self, item: Transport) -> None:
        ...
