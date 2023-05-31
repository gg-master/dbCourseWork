from dataclasses import dataclass
from typing import List
from db.entities import (
    Route,
    TransportWorker,
    RouteSchedule as EntityRouteSchedule,
)
from services.dto import Transport, TransportationStopSchedule


@dataclass
class RouteSchedule:
    id: int
    transport: Transport
    route: Route
    transport_workers: List[TransportWorker]
    included_stop_schedules: List[TransportationStopSchedule]

    @classmethod
    def from_entity(
        cls,
        route_schedule: EntityRouteSchedule,
        transport: Transport,
        route: Route,
        tr_workers: List[TransportWorker],
        stop_schedules: List[TransportationStopSchedule],
    ):
        return cls(
            route_schedule.id,
            transport,
            route,
            tr_workers,
            stop_schedules,
        )

    @classmethod
    def to_entity(self) -> EntityRouteSchedule:
        return EntityRouteSchedule(
            self.id,
            self.transport.id,
            self.route.id,
        )
