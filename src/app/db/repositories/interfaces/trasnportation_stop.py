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
    def create(self, item: TransportationStop) -> int:
        ...

    @abstractmethod
    def update(self, item: TransportationStop) -> None:
        ...

    @abstractmethod
    def create_conn_transportation_stop_transport_type(
        self, item_id: int, tr_types: List[TransportType]
    ):
        ...
    
    @abstractmethod
    def delete_conn_transportation_stop_transport_type(self, item_id: int):
        ...

    @abstractmethod
    def get_supported_transport_type(self, item_id: int) -> List[TransportType]:
        ...
