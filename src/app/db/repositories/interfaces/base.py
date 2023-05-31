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
    def create(self, item: Any) -> int:
        ...

    @abstractmethod
    def update(self, item: Any) -> None:
        ...

    @abstractmethod
    def delete(self, item_id: int) -> None:
        ...
