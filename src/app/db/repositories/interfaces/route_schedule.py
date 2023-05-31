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
    def create(self, item: RouteSchedule) -> int:
        ...

    @abstractmethod
    def update(self, item: RouteSchedule) -> None:
        ...

    @abstractmethod
    def create_conn_transport_workers_route_schedule(
        self, item_id: int, workers: List[TransportWorker]
    ):
        ...

    @abstractmethod
    def delete_conn_transport_workers_route_schedule(self, item_id: int):
        ...

    @abstractmethod
    def get_related_transport_workers(
        self, item_id: int
    ) -> List[TransportWorker]:
        ...
