from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    id: int
    email: str
    password_hash: str
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    phone: Optional[str] = None
    rut: Optional[str] = None
    avatar: Optional[str] = None
    birth_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()