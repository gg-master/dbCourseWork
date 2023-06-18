import logging
from typing import List
from app.services.dto import RouteSchedule
from app.db.repositories.interfaces import IRouteScheduleRepository
from app.db.implementations import UnitOfWork, PostgresDbConnector

from app.services.transport_service import TransportService
from app.services.transportation_stop_schedule_service import TransportationStopScheduleService
from app.services.route_service import RouteService


class RouteScheduleService:
    def __init__(
        self,
        route_schedule_repo: IRouteScheduleRepository,
        route_service: RouteService,
        transport_service: TransportService,
        tr_stop_schedule_service: TransportationStopScheduleService,
    ) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__route_schedule_repo = route_schedule_repo

        self.__route_service = route_service
        self.__transport_service = transport_service
        self.__tr_stop_schedule_service = tr_stop_schedule_service

    def get(self, item_id: int) -> RouteSchedule:
        route_schedule = self.__route_schedule_repo.get(item_id)
        transport = self.__transport_service.get(route_schedule.transport_id)
        route = self.__route_service.get(route_schedule.route_id)
        workers = self.__route_schedule_repo.get_related_transport_workers(
            item_id
        )
        included_stop_schedules = (
            self.__tr_stop_schedule_service.get_all_by_route_schedule(item_id)
        )
        return RouteSchedule.from_entity(
            route_schedule, transport, route, workers, included_stop_schedules
        )

    def get_all(self) -> List[RouteSchedule]:
        return list(
            map(
                lambda x: RouteSchedule.from_entity(
                    x,
                    self.__transport_service.get(x.transport_id),
                    self.__route_service.get(x.route_id),
                    self.__route_schedule_repo.get_related_transport_workers(
                        x.id
                    ),
                    self.__tr_stop_schedule_service.get_all_by_route_schedule(
                        x.id
                    ),
                ),
                self.__route_schedule_repo.get_all(),
            )
        )

    def create(self, item: RouteSchedule) -> None:
        with UnitOfWork(PostgresDbConnector):
            item.id = self.__route_schedule_repo.create(item.to_entity())
            self.__route_schedule_repo.create_conn_transport_workers_route_schedule(
                item.id, item.transport_workers
            )
            for stop_sched in item.included_stop_schedules:
                stop_sched.route_schedule.id = item.id
                self.__tr_stop_schedule_service.create(stop_sched)
            self.__logger.debug('Creating new RouteSchedule: %s', item)


    def update(self, item: RouteSchedule) -> None:
        with UnitOfWork(PostgresDbConnector):
            self.__route_schedule_repo.update(item.to_entity())
            self.__route_schedule_repo.delete_conn_transport_workers_route_schedule(
                item.id
            )
            self.__route_schedule_repo.create_conn_transport_workers_route_schedule(
                item.id, item.transport_workers
            )
            for stop_sched in self.__tr_stop_schedule_service.get_all_by_route_schedule(item.id):
                self.__tr_stop_schedule_service.delete(stop_sched.id)

            for stop_sched in item.included_stop_schedules:
                stop_sched.route_schedule.id = item.id
                self.__tr_stop_schedule_service.create(stop_sched)
            self.__logger.debug('Updating RouteSchedule: %s', item)


    def delete(self, item_id: int) -> None:
        with UnitOfWork(PostgresDbConnector):
            self.__route_schedule_repo.delete(item_id)
            self.__route_schedule_repo.delete_conn_transport_workers_route_schedule(
                item_id
            )
            for stop_sched in self.__tr_stop_schedule_service.get_all_by_route_schedule(item_id):
                self.__tr_stop_schedule_service.delete(stop_sched.id)
            self.__logger.debug('Deleting RouteSchedule with id: %s', item_id)
