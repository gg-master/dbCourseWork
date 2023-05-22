from typing import Any
from interfaces.user import IUserRepository


class UserRepository(IUserRepository):
    def get(self, item_id: int) -> Any:
        return super().get(item_id)
