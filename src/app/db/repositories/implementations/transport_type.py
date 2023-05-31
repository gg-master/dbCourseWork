from typing import List
from app.db.entities import TransportType
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import ITransportTypeRepository


class TransportTypeRepository(Repository, ITransportTypeRepository):
    def get(self, item_id: int) -> TransportType:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_type 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return TransportType(*self._cursor.fetchone())

    def get_all(self) -> List[TransportType]:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_type;
        """
        )
        return list(map(lambda x: TransportType(*x), self._cursor.fetchall()))

    def create(self, item: TransportType) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.transport_type(name)
	        VALUES (%(name)s)
            RETURNING id;
        """,
            {
                "name": item.name,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: TransportType) -> None:
        self._cursor.execute(
            """
            UPDATE public.transport_type SET name=%(name)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "name": item.name,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.transport_type
	            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
