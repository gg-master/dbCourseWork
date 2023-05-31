from abc import ABC, abstractmethod
from typing import List
from app.db.repositories.interfaces.base import IRepository
from app.db.entities import User


class IUserRepository(IRepository, ABC):
    @abstractmethod
    def get_all(self) -> List[User]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> User:
        ...

    @abstractmethod
    def create(self, item: User) -> int:
        ...

    @abstractmethod
    def update(self, item: User) -> None:
        ...
