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

    def create_conn_transport_workers_route_schedule(
        self, item_id: int, workers: List[TransportWorker]
    ):
        query = """
            INSERT INTO public.transport_workers_route_schedule(
                transport_workers_id, route_schedule_id)
                VALUES 
        """
        arr = [f'(%(tw{i})s, %(rs_id)' for i in range(len(workers))]
        query += ',\n'.join(arr) + ';'

        args = {"rs_id": item_id}
        i: TransportWorker
        for num, i in enumerate(workers):
            args[f'tw{num}'] = i.id

        self._cursor.execute(query, args)

    def delete_conn_transport_workers_route_schedule(self, item_id: int):
        self._cursor.execute(
            """
            DELETE FROM public.transport_workers_route_schedule
	            WHERE route_schedule_id = %(item_id)s;
        """,
            {"item_id": item_id},
        )

    def get_related_transport_workers(
        self, item_id: int
    ) -> List[TransportWorker]:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_workers tw
            JOIN transport_workers_route_schedule twrs 
            ON tw.id = twrs.transport_workers_id
            WHERE twrs.route_schedule_id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return list(
            map(lambda x: TransportWorker(*x), self._cursor.fetchall())
        )
