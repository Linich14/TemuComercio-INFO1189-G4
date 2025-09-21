from abc import ABC, abstractmethod
from typing import Optional, Any
from datetime import datetime

class TokenRepositoryInterface(ABC):

    @abstractmethod
    def save_refresh_token(self, user_id: int, token: str, expires_at: datetime ) -> None:
        pass

    @abstractmethod
    def revoke_token(self, token: str) -> None:
        pass

    @abstractmethod
    def find_refresh_token(self, token: str) -> Optional[dict[str, Any]]:
        pass
