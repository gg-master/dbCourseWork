from dataclasses import dataclass
from typing import List
from db.entities import Route
from services.dto import Transport, TransportationStop


@dataclass
class RouteSchedule:
    id: int
    transport: Transport
    route: Route
    included_stop_schedules = List[TransportationStop]
