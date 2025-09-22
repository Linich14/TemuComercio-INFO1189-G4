import secrets
import hashlib
import base64
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from typing import Any, Dict
from ...domain.services.auth_service import AuthServiceInterface
from ...domain.entities.auth_token import AuthToken
from ...domain.entities.user import User
from ...domain.repositories.token_repository import TokenRepositoryInterface
from ...domain.exceptions.auth_exceptions import (
    InvalidTokenException,
    TokenExpiredException
)

class DjangoAuthService(AuthServiceInterface):
    """Implementación Django del servicio de autenticación con tokens personalizados"""
    
    # Almacenamiento en memoria para access tokens
    _access_tokens = {}
    
    def __init__(self, token_repository: TokenRepositoryInterface):
        self.token_repository = token_repository
        self.access_token_expiry = timedelta(minutes=15)
        self.refresh_token_expiry = timedelta(days=30)
        self.secret_key = getattr(settings, 'SECRET_KEY', 'default-secret-key')
    
    def generate_tokens(self, user: User) -> AuthToken:
        """Genera tokens de acceso y refresco personalizados"""
        now = timezone.now()
        expires_at = now + self.access_token_expiry
        
        # Generar access token personalizado
        access_token = f"acc_{user.id}_{secrets.token_urlsafe(24)}"
        
        # Almacenar access token en memoria
        self._access_tokens[access_token] = {
            'user_id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'type': 'access',
            'created_at': now,
            'expires_at': expires_at
        }
        
        # Generar refresh token seguro
        refresh_token_value = self._generate_secure_token()
        
        # Guardar refresh token en base de datos
        self.token_repository.save_refresh_token(
            str(user.id), 
            refresh_token_value, 
            now + self.refresh_token_expiry
        )
        
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token_value,
            expires_at=int(expires_at.timestamp()),
            user_id=str(user.id)
        )
    
    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """Verifica y decodifica un token de acceso desde memoria"""
        if token not in self._access_tokens:
            raise InvalidTokenException("Access token inválido")
        
        token_data = self._access_tokens[token]
        
        # Verificar expiración
        if timezone.now() > token_data['expires_at']:
            # Limpiar token expirado
            del self._access_tokens[token]
            raise TokenExpiredException("Access token expirado")
        
        return token_data
    
    def verify_refresh_token(self, token: str) -> Dict[str, Any]:
        """Verifica refresh token desde base de datos"""
        token_data = self.token_repository.get_refresh_token(token)
        
        if not token_data:
            raise InvalidTokenException("Refresh token inválido")
        
        if not token_data.get('is_valid'):
            raise TokenExpiredException("Refresh token expirado o revocado")
        
        return token_data
    
    def refresh_access_token(self, refresh_token: str) -> AuthToken:
        """Renueva un token de acceso usando un refresh token"""
        # Verificar refresh token
        refresh_data = self.verify_refresh_token(refresh_token)
        user_id = refresh_data['user_id']
        
        # Generar nuevo access token
        now = timezone.now()
        expires_at = now + self.access_token_expiry
        access_token = f"acc_{user_id}_{secrets.token_urlsafe(24)}"
        
        # Necesitamos obtener los datos del usuario para el token
        # Esto debería venir del repositorio de usuarios
        from ...infrastructure.repositories.django_user_repository import DjangoUserRepository
        user_repo = DjangoUserRepository()
        user = user_repo.get_by_id(user_id)
        
        if not user:
            raise InvalidTokenException("Usuario no encontrado")
        
        # Almacenar nuevo access token en memoria
        self._access_tokens[access_token] = {
            'user_id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'type': 'access',
            'created_at': now,
            'expires_at': expires_at
        }
        
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token,  # Mantener el mismo refresh token
            expires_at=int(expires_at.timestamp()),
            user_id=str(user.id)
        )
    
    def revoke_token(self, token: str) -> bool:
        """Revoca un token"""
        # Intentar revocar como access token
        if token in self._access_tokens:
            del self._access_tokens[token]
            return True
        
        # Intentar revocar como refresh token
        return self.token_repository.revoke_refresh_token(token)
    
    def revoke_all_user_tokens(self, user_id: str):
        """Revoca todos los tokens de un usuario"""
        # Revocar access tokens en memoria
        tokens_to_remove = [
            token for token, data in self._access_tokens.items()
            if data['user_id'] == user_id
        ]
        
        for token in tokens_to_remove:
            del self._access_tokens[token]
        
        # Revocar refresh tokens en BD
        self.token_repository.revoke_all_user_tokens(user_id)
    
    def get_user_active_sessions(self, user_id: str) -> list:
        """Obtiene todas las sesiones activas de un usuario"""
        # Sesiones de access tokens
        access_sessions = [
            {
                'type': 'access',
                'token': token[:20] + '...',  # Mostrar solo parte del token
                'created_at': data['created_at'],
                'expires_at': data['expires_at']
            }
            for token, data in self._access_tokens.items()
            if data['user_id'] == user_id
        ]
        
        return access_sessions
    
    def cleanup_expired_tokens(self) -> int:
        """Limpia tokens expirados"""
        now = timezone.now()
        
        # Limpiar access tokens expirados de memoria
        expired_access = [
            token for token, data in self._access_tokens.items()
            if now > data['expires_at']
        ]
        
        for token in expired_access:
            del self._access_tokens[token]
        
        # Limpiar refresh tokens expirados de BD
        expired_refresh_count = self.token_repository.clean_expired_tokens()
        
        return len(expired_access) + expired_refresh_count
    
    def _generate_secure_token(self, length: int = 32) -> str:
        """Genera token seguro para refresh tokens"""
        random_bytes = secrets.token_bytes(length)
        timestamp = str(timezone.now().timestamp())
        hash_input = random_bytes + timestamp.encode() + self.secret_key.encode()
        token_hash = hashlib.sha256(hash_input).digest()
        combined = random_bytes + token_hash[:16]
        token = base64.urlsafe_b64encode(combined).decode('utf-8').rstrip('=')
        return f"ref_{secrets.token_urlsafe(8)}_{token}"
