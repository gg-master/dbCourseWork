from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import EmployeesPosition


class IEmployeesPositionRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[EmployeesPosition]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> EmployeesPosition:
        ...

    @abstractmethod
    def create(self, item: EmployeesPosition) -> int:
        ...

    @abstractmethod
    def update(self, item: EmployeesPosition) -> None:
        ...
