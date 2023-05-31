from typing import List
from app.db.entities import EmployeesPosition
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import IEmployeesPositionRepository


class EmployeesPositionRepository(Repository, IEmployeesPositionRepository):
    def get(self, item_id: int) -> EmployeesPosition:
        self._cursor.execute(
            """
            SELECT * FROM public.employees_positions 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return EmployeesPosition(*self._cursor.fetchone())

    def get_all(self) -> List[EmployeesPosition]:
        self._cursor.execute(
            """
            SELECT * FROM public.employees_positions;
        """
        )
        return list(
            map(lambda x: EmployeesPosition(*x), self._cursor.fetchall())
        )

    def create(self, item: EmployeesPosition) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.employees_positions(name, description)
	        VALUES (%(name)s, %(description)s)
            RETURNING id;
        """,
            {
                "name": item.name,
                "description": item.description,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: EmployeesPosition) -> None:
        self._cursor.execute(
            """
            UPDATE public.employees_positions
	            SET name=%(name)s, description=%(description)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "name": item.name,
                "description": item.description,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.employees_positions
	            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
