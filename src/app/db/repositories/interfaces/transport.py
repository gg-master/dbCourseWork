from abc import ABC, abstractmethod
from base import IRepository


class ITransportRepository(IRepository, ABC):
    pass
