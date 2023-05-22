from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    id: int
    full_name: str
    email: str
    phone: str
    birth_data: str
    registration_date: date
