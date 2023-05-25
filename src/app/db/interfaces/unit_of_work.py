from abc import ABC, abstractmethod


class IUnitOfWork(ABC):
    @abstractmethod
    def commit(self):
        ...

    @abstractmethod
    def rollback(self):
        ...

    @abstractmethod
    def __enter__(self):
        ...
    
    @abstractmethod
    def __exit__(self, ex_type, ex_value, ex_traceback):
        ...
