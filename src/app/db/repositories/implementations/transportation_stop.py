from typing import List
from app.db.entities import TransportType, TransportationStop
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import ITransportationStopRepository


class TransportationStopRepository(Repository, ITransportationStopRepository):
    def get(self, item_id: int) -> TransportationStop:
        self._cursor.execute(
            """
            SELECT * FROM public.transportation_stop 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return TransportationStop(*self._cursor.fetchone())

    def get_all(self) -> List[TransportationStop]:
        self._cursor.execute(
            """
            SELECT * FROM public.transportation_stop;
        """
        )
        return list(
            map(lambda x: TransportationStop(*x), self._cursor.fetchall())
        )

    def create(self, item: TransportationStop) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.transportation_stop(name, latitude, longitude)
            VALUES (%(name)s, %(latitude)s, %(longitude)s)
            RETURNING id;
        """,
            {
                "name": item.name,
                "latitude": item.latitude,
                "longitude": item.longitude,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: TransportationStop) -> None:
        self._cursor.execute(
            """
            UPDATE public.transportation_stop
                SET name=%(name)s, latitude=%(latitude)s, longitude=%(longitude)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "name": item.name,
                "latitude": item.latitude,
                "longitude": item.longitude,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.transportation_stop
	            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )

    def create_conn_transportation_stop_transport_type(
        self, item_id: int, tr_types: List[TransportType]
    ):
        query = """
            INSERT INTO public.transportation_stop_transport_type(
                transportation_stop_id, transport_type_id)
                VALUES 
        """
        arr = [f'(%(stop_id)s, %(tt{i})' for i in range(len(tr_types))]
        query += ',\n'.join(arr) + ';'

        args = {"stop_id": item_id}
        i: TransportType
        for num, i in enumerate(tr_types):
            args[f'tt{num}'] = i.id

        self._cursor.execute(query, args)

    def delete_conn_transportation_stop_transport_type(self, item_id: int):
        self._cursor.execute(
            """
            DELETE FROM public.transportation_stop_transport_type
	            WHERE transportation_stop_id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        
    def get_supported_transport_type(self, item_id) -> List[TransportType]:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_type tt
            JOIN transportation_stop_transport_type tstt 
            ON tt.id = tstt.transport_type_id
            WHERE tstt.transportation_stop_id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return list(map(lambda x: TransportType(*x), self._cursor.fetchall()))
