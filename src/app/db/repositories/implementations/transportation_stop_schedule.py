from typing import List
from app.db.entities import TransportWorker, TransportationStopSchedule
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import (
    ITransportationStopScheduleRepository,
)


class TransportationStopScheduleRepository(
    Repository, ITransportationStopScheduleRepository
):
    def get(self, item_id: int) -> TransportationStopSchedule:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_stop_schedule 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return TransportationStopSchedule(*self._cursor.fetchone())

    def get_all(self) -> List[TransportationStopSchedule]:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_stop_schedule;
        """
        )
        return list(
            map(
                lambda x: TransportationStopSchedule(*x),
                self._cursor.fetchall(),
            )
        )

    def get_all_by_route_schedule(
        self, route_sch_id: int
    ) -> List[TransportationStopSchedule]:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_stop_schedule
            WHERE route_schedule_id = %(route_sch_id)s;
        """,
            {"route_sch_id": route_sch_id},
        )
        return list(
            map(
                lambda x: TransportationStopSchedule(*x),
                self._cursor.fetchall(),
            )
        )
    
    def get_all_by_tr_stop(self, tr_stop_id: int) -> List[TransportationStopSchedule]:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_stop_schedule
            WHERE stop_id = %(tr_stop_id)s;
        """,
            {"tr_stop_id": tr_stop_id},
        )
        return list(
            map(
                lambda x: TransportationStopSchedule(*x),
                self._cursor.fetchall(),
            )
        )

    def create(self, item: TransportationStopSchedule) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.transport_stop_schedule(
                route_schedule_id, stop_id, departure_time)
                VALUES (%(route_schedule_id)s, %(stop_id)s, %(departure_time)s)
            RETURNING id;
        """,
            {
                "route_schedule_id": item.route_schedule_id,
                "stop_id": item.stop_id,
                "departure_time": item.departure_time,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: TransportationStopSchedule) -> None:
        self._cursor.execute(
            """
            UPDATE public.transport_stop_schedule
                SET route_schedule_id=%(route_schedule_id)s, stop_id=%(stop_id)s, departure_time=%(departure_time)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "route_schedule_id": item.route_schedule_id,
                "stop_id": item.stop_id,
                "departure_time": item.departure_time,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.transport_stop_schedule
	            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
