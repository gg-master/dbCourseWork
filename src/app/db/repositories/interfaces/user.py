from abc import ABC, abstractmethod
from base import IRepository


class IUserRepository(IRepository, ABC):
    pass
