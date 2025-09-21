# core/application/dtos/auth_dto.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class LoginRequestDTO:
    email: str
    password: str

@dataclass
class RegisterRequestDTO:
    email: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    rut: Optional[str] = None
    birth_date: Optional[datetime] = None

@dataclass
class AuthResponseDTO:
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: int
    user: dict
    
    @classmethod
    def from_user_and_tokens(cls, user: 'User', tokens: 'AuthToken'):
        return cls(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
            expires_at=tokens.expires_at,
            user={
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'rut': user.rut,
                'avatar': user.avatar,
                'is_verified': user.is_verified,
                'last_login': user.last_login.isoformat() if user.last_login else None
            }
        )

@dataclass
class UserResponseDTO:
    id: int
    email: str
    full_name: str
    first_name: str
    last_name: str
    phone: Optional[str]
    rut: Optional[str]
    avatar: Optional[str]
    is_verified: bool
    
    @classmethod
    def from_user(cls, user: 'User'):
        return cls(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            rut=user.rut,
            avatar=user.avatar,
            is_verified=user.is_verified
        )