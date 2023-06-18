from dataclasses import dataclass
from datetime import date
from typing import List
from app.db.entities.transport_worker import TransportWorker as EntityTW
from app.db.entities.employees_position import EmployeesPosition


@dataclass
class TransportWorker:
    id: int
    full_name: str
    phone: str
    birth_date: date
    positions: List[EmployeesPosition]

    @classmethod
    def from_entity(
        cls, transport_worker: EntityTW, positions: List[EmployeesPosition]
    ):
        return cls(
            transport_worker.id,
            transport_worker.full_name,
            transport_worker.phone,
            transport_worker.birth_date,
            positions,
        )

    def to_entity(self) -> EntityTW:
        return EntityTW(self.id, self.full_name, self.phone, self.birth_date)

    def to_dict(self) -> dict:
        worker_dict = self.__dict__
        worker_dict['positions'] = list(
            map(lambda x: x.to_dict(), self.positions)
        )
        return worker_dict

    @classmethod
    def from_json(cls, item_dict: dict) -> 'TransportWorker':
        return cls(
            item_dict.get("id"),
            item_dict.get("full_name"),
            item_dict.get("phone"),
            item_dict.get("birth_date"),
            list(
                map(
                    lambda x: EmployeesPosition(
                        x.get("id"),
                        x.get("name"),
                        x.get("description"),
                    ),
                    item_dict.get("positions"),
                )
            ),
        )
