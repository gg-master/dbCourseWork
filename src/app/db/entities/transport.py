from dataclasses import dataclass
from datetime import date


@dataclass
class Transport:
    id: int
    brand: str
    registration_number: str
    manufacturer: str
    manufacturing_date: date
    capacity: int
    is_repaired: bool
    type_id: int
