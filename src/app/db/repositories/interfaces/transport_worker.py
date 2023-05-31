from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import TransportWorker


class ITransportWorkerRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[TransportWorker]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> TransportWorker:
        ...

    @abstractmethod
    def create(self, item: TransportWorker) -> int:
        ...

    @abstractmethod
    def update(self, item: TransportWorker) -> None:
        ...
