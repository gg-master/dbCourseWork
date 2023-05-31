from dataclasses import dataclass
from datetime import datetime
from db.entities import (
    RouteSchedule,
    TransportationStopSchedule as EntityTrStopSchedule,
)
from services.dto import TransportationStop


@dataclass
class TransportationStopSchedule:
    id: int
    route_schedule: RouteSchedule
    stop: TransportationStop
    departure_time: datetime

    @classmethod
    def from_entity(
        cls,
        tr_stop_schedule: EntityTrStopSchedule,
        route_schedule: RouteSchedule,
        transportation_stop: TransportationStop
    ):
        return cls(
            tr_stop_schedule.id,
            route_schedule,
            transportation_stop,
            tr_stop_schedule.departure_time,
        )

    def to_entity(self) -> EntityTrStopSchedule:
        return EntityTrStopSchedule(
            self.id,
            self.route_schedule.id,
            self.stop.id,
            self.departure_time,
        )
