from abc import ABC, abstractmethod
from typing import Any
from ..entities import AuthToken, User


class AuthServiceInterface(ABC):

    @abstractmethod
    def generate_tokens(self, user: User) -> AuthToken:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> dict[str, Any]:
        pass