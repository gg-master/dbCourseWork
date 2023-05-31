import logging
from typing import List
from app.services.dto import TransportationStopSchedule
from app.db.repositories.interfaces import (
    ITransportationStopScheduleRepository,
    IRouteScheduleRepository,
)
from app.db.implementations import UnitOfWork, Database
from app.services.transportation_stop_service import TransportationStopService


class TransportationStopScheduleService:
    def __init__(
        self,
        tr_stop_schedule_repo: ITransportationStopScheduleRepository,
        route_schedule_repo: IRouteScheduleRepository,
        transportation_stop_service: TransportationStopService,
    ) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__tr_stop_schedule_repo = tr_stop_schedule_repo
        self.__route_schedule_repo = route_schedule_repo
        self.__tr_stop_service = transportation_stop_service

    def get(self, item_id: int) -> TransportationStopSchedule:
        tr_stop_schedule = self.__tr_stop_schedule_repo.get(item_id)
        route_schedule = self.__route_schedule_repo.get(
            tr_stop_schedule.route_schedule_id
        )
        tr_stop = self.__tr_stop_service.get(tr_stop_schedule.stop_id)

        return TransportationStopSchedule.from_entity(
            tr_stop_schedule, route_schedule, tr_stop
        )

    def get_all(self) -> List[TransportationStopSchedule]:
        return list(
            map(
                lambda x: TransportationStopSchedule.from_entity(
                    x,
                    self.__route_schedule_repo.get(x.route_schedule_id),
                    self.__tr_stop_service.get(x.stop_id),
                ),
                self.__tr_stop_schedule_repo.get_all(),
            )
        )

    def get_all_by_route_schedule(
        self, route_sch_id: int
    ) -> List[TransportationStopSchedule]:
        return list(
            map(
                lambda x: TransportationStopSchedule.from_entity(
                    x,
                    self.__route_schedule_repo.get(x.route_schedule_id),
                    self.__tr_stop_service.get(x.stop_id),
                ),
                self.__tr_stop_schedule_repo.get_all_by_route_schedule(route_sch_id),
            )
        )

    def create(self, item: TransportationStopSchedule) -> None:
        with UnitOfWork(Database):
            self.__tr_stop_schedule_repo.create(item.to_entity())

    def update(self, item: TransportationStopSchedule) -> None:
        with UnitOfWork(Database):
            self.__tr_stop_schedule_repo.update(item.to_entity())

    def delete(self, item_id: int) -> None:
        with UnitOfWork(Database):
            self.__tr_stop_schedule_repo.delete(item_id)
