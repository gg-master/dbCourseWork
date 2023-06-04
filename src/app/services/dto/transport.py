import json
from dataclasses import dataclass
from datetime import date
from app.db.entities import TransportType, Transport as EntityTransport


@dataclass
class Transport:
    id: int
    brand: str
    registration_number: str
    manufacturer: str
    manufacturing_date: date
    capacity: int
    is_repaired: bool
    transport_type: TransportType

    @classmethod
    def from_entity(cls, transport: EntityTransport, tr_type: TransportType):
        return cls(
            transport.id,
            transport.brand,
            transport.registration_number,
            transport.manufacturer,
            transport.manufacturing_date,
            transport.capacity,
            transport.is_repaired,
            tr_type,
        )

    def to_entity(self) -> EntityTransport:
        return EntityTransport(
            self.id,
            self.brand,
            self.registration_number,
            self.manufacturer,
            self.manufacturing_date,
            self.capacity,
            self.is_repaired,
            self.transport_type.id,
        )

    def to_dict(self) -> dict:
        transport_dict = self.__dict__
        transport_dict['manufacturing_date'] = self.manufacturing_date.isoformat()
        transport_dict['transport_type'] = self.transport_type.__dict__
        return transport_dict

    @classmethod
    def from_json(cls, item_dict: dict) -> 'Transport':
        return cls(
            item_dict.get("id"),
            item_dict.get("brand"),
            item_dict.get("registration_number"),
            item_dict.get("manufacturer"),
            item_dict.get("manufacturing_date"),
            item_dict.get("capacity"),
            item_dict.get("is_repaired"),
            TransportType(
                item_dict.get("transport_type").get("id"),
                item_dict.get("transport_type").get("name"),
            )
        )
