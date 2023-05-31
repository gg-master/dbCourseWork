from typing import List
from app.db.entities import Route
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import IRouteRepository


class RouteRepository(Repository, IRouteRepository):
    def get(self, item_id: int) -> Route:
        self._cursor.execute(
            """
            SELECT * FROM public.routes 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return Route(*self._cursor.fetchone())

    def get_all(self) -> List[Route]:
        self._cursor.execute(
            """
            SELECT * FROM public.routes;
        """
        )
        return list(map(lambda x: Route(*x), self._cursor.fetchall()))

    def create(self, item: Route) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.routes(name, price, rating)
	        VALUES (%(name)s, %(price)s, %(rating)s)
            RETURNING id;
        """,
            {
                "name": item.name,
                "price": item.price,
                "rating": item.rating,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: Route) -> None:
        self._cursor.execute(
            """
            UPDATE public.routes
	            SET name=%(name)s, price=%(price)s, rating=%(rating)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "price": item.price,
                "rating": item.rating,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.routes
	            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
