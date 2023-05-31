from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import TransportType


class ITransportTypeRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[TransportType]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> TransportType:
        ...

    @abstractmethod
    def create(self, item: TransportType) -> int:
        ...

    @abstractmethod
    def update(self, item: TransportType) -> None:
        ...
