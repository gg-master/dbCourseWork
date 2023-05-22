from dataclasses import dataclass
from typing import List
from db.entities import TransportWorker


@dataclass
class EmployeesPosition:
    id: int
    name: str
    description: str
    available_workers: List[TransportWorker]
