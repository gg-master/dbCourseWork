from dataclasses import dataclass
from datetime import date

from db.entities import TransportType


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
