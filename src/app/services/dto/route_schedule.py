from dataclasses import dataclass
from typing import List
from app.db.entities import (
    Route,
    TransportWorker,
    RouteSchedule as EntityRouteSchedule,
)
from app.db.entities.transport_type import TransportType
from app.services.dto.transport import Transport
from app.services.dto.transport_stop_schedule import TransportationStopSchedule
from app.services.dto.transportation_stop import TransportationStop


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

    def to_entity(self) -> EntityRouteSchedule:
        return EntityRouteSchedule(
            self.id,
            self.transport.id,
            self.route.id,
        )

    def to_dict(self) -> dict:
        route_schedule = self.__dict__
        route_schedule['transport'] = self.transport.to_dict()
        route_schedule['included_stop_schedules'] = list(
            map(lambda x: x.to_dict(), self.included_stop_schedules)
        )
        return route_schedule

    @classmethod
    def from_dict(cls, item_dict: dict) -> 'Transport':
        return cls(
            item_dict.get("id"),
            Transport.from_dict(item_dict.get("transport")),
            Route(
                item_dict.get("route").get("id"),
                item_dict.get("route").get("name"),
                item_dict.get("route").get("price"),
                item_dict.get("route").get("rating"),
            ),
            list(
                map(
                    lambda x: TransportWorker(
                        x.get("id"),
                        x.get("full_name"),
                        x.get("phone"),
                        x.get("birth_date"),
                    ),
                    item_dict.get("transport_workers"),
                )
            ),
            list(
                map(
                    lambda x: TransportationStopSchedule(
                        x.get("id"),
                        EntityRouteSchedule(
                            x.get("route_schedule", {}).get("id"),
                            x.get("route_schedule", {}).get("transport_id"),
                            x.get("route_schedule", {}).get("route_id"),
                        ),
                        TransportationStop.from_dict(
                            x.get("transportation_stop")
                        ),
                        x.get("departure_time"),
                    ),
                    item_dict.get("included_stop_schedules"),
                )
            ),
        )
