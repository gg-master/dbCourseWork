from dataclasses import dataclass


@dataclass
class TransportationStop:
    id: int
    name: str
    latitude: float
    longitude: float
