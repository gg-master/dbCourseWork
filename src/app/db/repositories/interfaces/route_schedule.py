from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import RouteSchedule, TransportWorker


class IRouteScheduleRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[RouteSchedule]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> RouteSchedule:
        ...

    @abstractmethod
    def add(self, item: RouteSchedule) -> int:
        ...

    @abstractmethod
    def update(self, item: RouteSchedule) -> None:
        ...

    @abstractmethod
    def add_connection_transport_workers_route_schedule(
        self, item_id: int, tr_workers: List[TransportWorker]
    ) -> None:
        ...
