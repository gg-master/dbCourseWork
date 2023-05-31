import logging
from typing import List
from app.services.dto import Transport
from app.db.repositories.interfaces import (
    ITransportRepository,
    ITransportTypeRepository,
)
from app.db.implementations import UnitOfWork, Database


class TransportService:
    def __init__(
        self,
        transport_repo: ITransportRepository,
        type_repo: ITransportTypeRepository,
    ) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__transport_repo = transport_repo
        self.__type_repo = type_repo

    def get(self, item_id: int) -> Transport:
        transport = self.__transport_repo.get(item_id)
        tr_type = self.__type_repo.get(transport.type_id)
        return Transport.from_entity(transport, tr_type)

    def get_all(self) -> List[Transport]:
        return list(
            map(
                lambda x: Transport.from_entity(
                    x, self.__type_repo.get(x.type_id)
                ),
                self.__transport_repo.get_all(),
            )
        )

    def create(self, item: Transport) -> None:
        with UnitOfWork(Database):
            self.__transport_repo.create(item.to_entity())

    def update(self, item: Transport) -> None:
        with UnitOfWork(Database):
            self.__transport_repo.update(item.to_entity())

    def delete(self, item_id: int) -> None:
        with UnitOfWork(Database):
            self.__transport_repo.delete(item_id)
