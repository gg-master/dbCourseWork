from dataclasses import dataclass
from typing import List
from app.db.entities.transport_worker import TransportWorker


@dataclass
class EmployeesPosition:
    id: int
    name: str
    description: str
    available_workers: List[TransportWorker]
