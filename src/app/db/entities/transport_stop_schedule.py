from dataclasses import dataclass
from datetime import datetime


@dataclass
class TransportStopSchedule:
    id: int
    route_schedule_id: id
    stop_id: int
    departure_time: datetime
