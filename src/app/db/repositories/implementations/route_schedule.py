from typing import List
from app.db.entities import RouteSchedule, TransportWorker
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import IRouteScheduleRepository


class RouteScheduleRepository(Repository, IRouteScheduleRepository):
    def get(self, item_id: int) -> RouteSchedule:
        self._cursor.execute(
            """
            SELECT * FROM public.route_schedule 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return RouteSchedule(*self._cursor.fetchone())

    def get_all(self) -> List[RouteSchedule]:
        self._cursor.execute(
            """
            SELECT * FROM public.route_schedule;
        """
        )
        return list(map(lambda x: RouteSchedule(*x), self._cursor.fetchall()))

    def create(self, item: RouteSchedule) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.route_schedule(transport_id, route_id)
            VALUES (%(transport_id)s, %(route_id)s)
            RETURNING id;
        """,
            {
                "transport_id": item.transport_id,
                "route_id": item.route_id,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: RouteSchedule) -> None:
        self._cursor.execute(
            """
            UPDATE public.route_schedule
	            SET transport_id=%(transport_id)s, route_id=%(route_id)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "transport_id": item.transport_id,
                "route_id": item.route_id,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.route_schedule
	            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )

    def create_connection_transport_workers_route_schedule(
        self, item_id: int, tr_workers: List[TransportWorker]
    ) -> None:
        query = """
            INSERT INTO public.transport_workers_route_schedule(
	            transport_workers_id, route_schedule_id)
                VALUES 
        """
        arr = [f'(%(tw{i})s, %(rs_id)' for i in range(len(tr_workers))]
        query += ',\n'.join(arr) + ';'

        args = {"rs_id": item_id}
        i: TransportWorker
        for num, i in enumerate(tr_workers):
            args[f'tw{num}'] = i.id

        self._cursor.execute(query, args)
