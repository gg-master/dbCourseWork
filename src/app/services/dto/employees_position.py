from dataclasses import dataclass
from typing import List
from app.db.entities.transport_worker import TransportWorker


@dataclass
class EmployeesPosition:
    id: int
    name: str
    description: str
    available_workers: List[TransportWorker]

    def to_dict(self) -> dict:
        transport_dict = self.__dict__
        transport_dict['available_workers'] = list(
            map(lambda x: x.to_dict(), self.available_workers)
        )
        return transport_dict

    @classmethod
    def from_json(cls, item_dict: dict) -> 'EmployeesPosition':
        return cls(
            item_dict.get("id"),
            item_dict.get("name"),
            item_dict.get("description"),
            list(
                map(
                    lambda x: TransportWorker(
                        x.get("id"),
                        x.get("full_name"),
                        x.get("phone"),
                        x.get("birth_date"),
                    ),
                    item_dict.get("available_workers"),
                )
            ),
        )
