from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import TransportationStop, TransportType


class ITransportationStopRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[TransportationStop]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> TransportationStop:
        ...

    @abstractmethod
    def add(self, item: TransportationStop) -> int:
        ...

    @abstractmethod
    def update(self, item: TransportationStop) -> None:
        ...

    @abstractmethod
    def add_connection_transportation_stop_transport_type(
        self, item_id: int, tr_types: List[TransportType]
    ):
        ...
