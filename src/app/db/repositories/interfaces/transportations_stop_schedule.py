from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import TransportationStopSchedule


class ITransportationStopScheduleRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[TransportationStopSchedule]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> TransportationStopSchedule:
        ...

    @abstractmethod
    def create(self, item: TransportationStopSchedule) -> int:
        ...

    @abstractmethod
    def update(self, item: TransportationStopSchedule) -> None:
        ...

    @abstractmethod
    def get_all_by_route_schedule(
        self, route_sch_id: int
    ) -> List[TransportationStopSchedule]:
        ...
