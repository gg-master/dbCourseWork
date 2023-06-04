import logging
from typing import List
from app.services.dto import TransportationStop
from app.db.repositories.interfaces import ITransportationStopRepository
from app.db.implementations import UnitOfWork, PostgresDbConnector


class TransportationStopService:
    def __init__(self, tr_stop_repo: ITransportationStopRepository) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__tr_stop_repo = tr_stop_repo

    def get(self, item_id: int) -> TransportationStop:
        transport = self.__tr_stop_repo.get(item_id)
        tr_type = self.__tr_stop_repo.get_supported_transport_type(item_id)
        return TransportationStop.from_entity(transport, tr_type)

    def get_all(self) -> List[TransportationStop]:
        return list(
            map(
                lambda x: TransportationStop.from_entity(
                    x,
                    self.__tr_stop_repo.get_supported_transport_type(
                        x.type_id
                    ),
                ),
                self.__tr_stop_repo.get_all(),
            )
        )

    def create(self, item: TransportationStop) -> None:
        with UnitOfWork(PostgresDbConnector):
            self.__tr_stop_repo.create(item.to_entity())
            self.__tr_stop_repo.create_conn_transportation_stop_transport_type(
                item.id, item.supported_transport_types
            )

    def update(self, item: TransportationStop) -> None:
        with UnitOfWork(PostgresDbConnector):
            self.__tr_stop_repo.update(item.to_entity())
            self.__tr_stop_repo.delete_conn_transportation_stop_transport_type(
                item.id
            )
            self.__tr_stop_repo.create_conn_transportation_stop_transport_type(
                item.id, item.supported_transport_types
            )

    def delete(self, item_id: int) -> None:
        with UnitOfWork(PostgresDbConnector):
            self.__tr_stop_repo.delete(item_id)
            self.__tr_stop_repo.delete_conn_transportation_stop_transport_type(
                item_id
            )
