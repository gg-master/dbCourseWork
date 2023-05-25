from abc import ABC, abstractmethod

from app.misc.singleton import SingletonMeta


class IDatabase(ABC):
    __metaclass__ = SingletonMeta
    @classmethod
    @abstractmethod
    def get_connection(cls):
        ...

    @classmethod
    @abstractmethod
    def _create_connection(cls):
        ...

    @classmethod
    @abstractmethod
    def dispose_connection(cls):
        ...
