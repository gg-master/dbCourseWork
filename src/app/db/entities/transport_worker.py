from dataclasses import dataclass
from datetime import date


@dataclass
class TransportWorker:
    id: int
    full_name: str
    phone: str
    birth_date: date
 