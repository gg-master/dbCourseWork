from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import TransportStopSchedule


class ITransportationStopScheduleRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[TransportStopSchedule]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> TransportStopSchedule:
        ...

    @abstractmethod
    def add(self, item: TransportStopSchedule) -> int:
        ...

    @abstractmethod
    def update(self, item: TransportStopSchedule) -> None:
        ...
