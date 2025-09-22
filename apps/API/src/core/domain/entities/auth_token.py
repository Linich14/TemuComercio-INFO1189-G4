from dataclasses import dataclass

@dataclass
class AuthToken:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600 
