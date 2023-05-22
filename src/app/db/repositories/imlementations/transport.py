from abc import ABC, abstractmethod
from interfaces.transport import ITransportRepository


class TransportRepository(ITransportRepository, ABC):
    pass
