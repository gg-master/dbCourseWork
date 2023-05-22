from abc import ABC, abstractmethod
from typing import Any, List
from base import IRepository


class IUserRepository(IRepository, ABC):
    def get_all(self) -> List[Any]:
        return super().get_all()
