from dataclasses import dataclass
from typing import List
from db.entities import TransportType


@dataclass
class TransportationStop:
    id: int
    name: str
    latitude: float
    longitude: float
    supported_transport_types: List[TransportType]
