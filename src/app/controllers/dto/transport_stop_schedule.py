from dataclasses import dataclass
from datetime import datetime
from services.dto.route_schedule import RouteSchedule, TransportationStop


@dataclass
class TransportatStopSchedule:
    id: int
    route_schedule: RouteSchedule
    stop: TransportationStop
    departure_time: datetime
