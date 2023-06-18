from typing import List
from app.db.entities import Transport
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import ITransportRepository


class TransportRepository(Repository, ITransportRepository):
    def get(self, item_id: int) -> Transport:
        self._cursor.execute(
            """
            SELECT * FROM public.transport 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return Transport(*self._cursor.fetchone())

    def get_all(self) -> List[Transport]:
        self._cursor.execute(
            """
            SELECT * FROM public.transport;
        """
        )
        return list(map(lambda x: Transport(*x), self._cursor.fetchall()))

    def create(self, item: Transport) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.transport(brand, registration_number, 
                manufacturer, manufacturing_date, capacity, 
                is_repaired, type_id)
	        VALUES (%(brand)s, %(registration_number)s, %(manufacturer)s, 
            %(manufacturing_date)s, %(capacity)s, %(is_repaired)s, %(type_id)s)
            RETURNING id;
        """,
            {
                "brand": item.brand,
                "registration_number": item.registration_number,
                "manufacturer": item.manufacturer,
                "manufacturing_date": item.manufacturing_date,
                "capacity": item.capacity,
                "is_repaired": item.is_repaired,
                "type_id": item.type_id,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: Transport) -> None:
        self._cursor.execute(
            """
            UPDATE public.transport
                SET brand=%(brand)s, registration_number=%(registration_number)s, 
                manufacturer=%(manufacturer)s, manufacturing_date=%(manufacturing_date)s, 
                capacity=%(capacity)s, is_repaired=%(is_repaired)s, type_id=%(type_id)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "brand": item.brand,
                "registration_number": item.registration_number,
                "manufacturer": item.manufacturer,
                "manufacturing_date": item.manufacturing_date,
                "capacity": item.capacity,
                "is_repaired": item.is_repaired,
                "type_id": item.type_id,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.transport
	            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
