from typing import List
from app.db.entities import TransportWorker
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import ITransportWorkerRepository


class TransportWorkerRepository(Repository, ITransportWorkerRepository):
    def get(self, item_id: int) -> TransportWorker:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_workers 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return TransportWorker(*self._cursor.fetchone())

    def get_all(self) -> List[TransportWorker]:
        self._cursor.execute(
            """
            SELECT * FROM public.transport_workers;
        """
        )
        return list(
            map(lambda x: TransportWorker(*x), self._cursor.fetchall())
        )

    def create(self, item: TransportWorker) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.transport_workers(full_name, phone, birth_date)
	        VALUES (%(full_name)s, %(phone)s, %(birth_date)s)
            RETURNING id;
        """,
            {
                "full_name": item.full_name,
                "phone": item.phone,
                "birth_date": item.birth_date,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: TransportWorker) -> None:
        self._cursor.execute(
            """
            UPDATE public.transport_workers
	            SET full_name=%(full_name)s, phone=%(phone)s, birth_date=%(birth_date)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "full_name": item.full_name,
                "phone": item.phone,
                "birth_date": item.birth_date,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.transport_workers
	            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
