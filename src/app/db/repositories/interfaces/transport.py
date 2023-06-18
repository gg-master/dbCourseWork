from abc import ABC, abstractmethod
from datetime import date
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
    def create(self, item: Transport) -> int:
        ...

    @abstractmethod
    def update(self, item: Transport) -> None:
        ...

    @abstractmethod
    def get_all_transport_from_manufacturing_date(
        self, manufacturing_date: date
    ) -> List[Transport]:
        ...
