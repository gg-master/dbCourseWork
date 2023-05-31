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
