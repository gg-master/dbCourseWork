from abc import ABC, abstractmethod
from typing import Any, List


class IRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Any]:
        ...

    @abstractmethod
    def get(self, item_id: int) -> Any:
        ...

    @abstractmethod
    def add(self, item: Any) -> None:
        ...

    @abstractmethod
    def update(self, item: Any) -> None:
        ...
