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

    def to_dict(self) -> dict:
        transport_dict = self.__dict__
        transport_dict['supported_transport_types'] = list(
            map(lambda x: x.to_dict(), self.supported_transport_types)
        )
        return transport_dict

    @classmethod
    def from_dict(cls, item_dict: dict) -> 'TransportationStop':
        return cls(
            item_dict.get("id"),
            item_dict.get("name"),
            item_dict.get("latitude"),
            item_dict.get("longitude"),
            list(
                map(
                    lambda x: TransportType(
                        x.get("id"),
                        x.get("name"),
                    ),
                    item_dict.get("supported_transport_types"),
                )
            ),
        )
