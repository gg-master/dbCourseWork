from typing import List
from app.db.entities import User
from app.db.repositories.implementations.base import Repository
from app.db.repositories.interfaces import IUserRepository


class UserRepository(Repository, IUserRepository):
    def get(self, item_id: int) -> User:
        self._cursor.execute(
            """
            SELECT * FROM public.users 
            WHERE id = %(item_id)s;
        """,
            {"item_id": item_id},
        )
        return User(*self._cursor.fetchone())

    def get_all(self) -> List[User]:
        self._cursor.execute(
            """
            SELECT * FROM public.users;
        """
        )
        return list(map(lambda x: User(*x), self._cursor.fetchall()))

    def add(self, item: User) -> int:
        self._cursor.execute(
            """
            INSERT INTO public.users(
	            full_name, email, phone, birth_date, registration_date)
	            VALUES 
                (%(full_name)s, %(email)s, %(phone)s, 
                %(birth_date)s, %(registration_date)s)
                RETURNING id;
        """,
            {
                "full_name": item.full_name,
                "email": item.email,
                "phone": item.phone,
                "birth_date": item.birth_date,
                "registration_date": item.registration_date,
            },
        )
        return self._cursor.fetchone()[0]

    def update(self, item: User) -> None:
        self._cursor.execute(
            """
            UPDATE public.users
                SET full_name=%(full_name)s, email=%(email)s, phone=%(phone)s, 
                birth_date=%(birth_date)s, registration_date=%(registration_date)s
                WHERE id = %(item_id)s;
        """,
            {
                "item_id": item.id,
                "full_name": item.full_name,
                "email": item.email,
                "phone": item.phone,
                "birth_date": item.birth_date,
                "registration_date": item.registration_date,
            },
        )

    def delete(self, item_id: int) -> None:
        self._cursor.execute(
            """
            DELETE FROM public.users
	            WHERE id = %(item_id)s;
        """,
            {
                "item_id": item_id
            },
        )
