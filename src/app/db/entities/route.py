from dataclasses import dataclass


@dataclass
class Route:
    id: int
    name: str
    price: float
    rating: float
