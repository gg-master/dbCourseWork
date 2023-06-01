from dataclasses import dataclass
from typing import List
from app.db.entities import TransportType, TransportationStop as EntityTrStop


@dataclass
class TransportationStop:
    id: int
    name: str
    latitude: float
    longitude: float
    supported_transport_types: List[TransportType]

    @classmethod
    def from_entity(
        cls,
        tr_stop: EntityTrStop,
        supported_transport_types: List[TransportType],
    ):
        return cls(
            tr_stop.id,
            tr_stop.name,
            tr_stop.latitude,
            tr_stop.longitude,
            supported_transport_types,
        )

    def to_entity(self) -> EntityTrStop:
        return EntityTrStop(
            self.id,
            self.name,
            self.latitude,
            self.longitude,
        )
