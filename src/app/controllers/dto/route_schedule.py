from dataclasses import dataclass
from typing import List
from db.entities import Route, TransportWorker
from services.dto import Transport, TransportationStop


@dataclass
class RouteSchedule:
    id: int
    transport: Transport
    route: Route
    transport_workers: List[TransportWorker]
    included_stop_schedules: List[TransportationStop]
