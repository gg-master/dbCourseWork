from dataclasses import dataclass


@dataclass
class RouteSchedule:
    id: int
    transport_id: int
    route_id: int
