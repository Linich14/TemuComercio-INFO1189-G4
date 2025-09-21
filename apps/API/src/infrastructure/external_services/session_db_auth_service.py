import secrets
import hashlib
import base64
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from ...core.domain.services.auth_service import AuthServiceInterface
from ...core.domain.entities.user import User
from ...core.domain.entities.auth_token import AuthToken
from ...core.domain.exceptions.auth_exceptions import *
from ..models.token_model import RefreshToken
from ...core.domain.entities.user import User as DomainUser


class SessionDBAuthService(AuthServiceInterface):
   
    _access_tokens = {}
    
    def __init__(self):
        self.access_token_expiry = timedelta(minutes=15)
        self.refresh_token_expiry = timedelta(days=30)
        self.secret_key = settings.SECRET_KEY
    
    def generate_tokens(self, user: DomainUser) -> AuthToken:  # Usar DomainUser
        now = timezone.now()
        expires_at = now + self.access_token_expiry
        
        access_token = f"acc_{user.id}_{secrets.token_urlsafe(24)}"
        
        self._access_tokens[access_token] = {
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'type': 'access',
            'created_at': now,
            'expires_at': expires_at
        }
        
        refresh_token_value = self._generate_secure_token()
        
        refresh_token_obj = RefreshToken.objects.create(
            user_id=user.id,
            token=refresh_token_value,
            expires_at=now + self.refresh_token_expiry,
            revoked=False
        )
        
        return AuthToken(
            access_token=access_token,
            refresh_token=refresh_token_value,
            expires_at=int(expires_at.timestamp())
        )
    
    def verify_access_token(self, token: str) -> dict:
        """Verificar access token desde memoria"""
        if token not in self._access_tokens:
            raise InvalidTokenException("Access token inválido")
        
        token_data = self._access_tokens[token]
        
        # Verificar expiración
        if timezone.now() > token_data['expires_at']:
            # Limpiar token expirado
            del self._access_tokens[token]
            raise TokenExpiredException("Access token expirado")
        
        return token_data
    
    def verify_refresh_token(self, token: str) -> dict:
        """Verificar refresh token desde base de datos"""
        try:
            refresh_token = RefreshToken.objects.get(
                token=token,
                revoked=False
            )
            
            if refresh_token.is_expired():
                refresh_token.revoked = True
                refresh_token.save()
                raise TokenExpiredException("Refresh token expirado")
            
            return {
                'user_id': refresh_token.user.id,
                'token_id': str(refresh_token.id),
                'created_at': refresh_token.created_at,
                'expires_at': refresh_token.expires_at
            }
            
        except RefreshToken.DoesNotExist:
            raise InvalidTokenException("Refresh token inválido")
    
    def refresh_access_token(self, refresh_token: str) -> AuthToken:
        """Generar nuevo access token usando refresh token"""
        refresh_data = self.verify_refresh_token(refresh_token)
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        try:
            django_user = User.objects.get(id=refresh_data['user_id'], is_active=True)
            
            user = DomainUser(
                id=django_user.id,
                email=django_user.email,
                password_hash=django_user.password,
                first_name=django_user.first_name,
                last_name=django_user.last_name,
                phone=django_user.phone,
                rut=django_user.rut,
                avatar=django_user.avatar,
                birth_date=django_user.birth_date,
                is_active=django_user.is_active,
                is_verified=django_user.is_verified,
                created_at=django_user.created_at,
                last_login=django_user.last_login
            )
            
            now = timezone.now()
            expires_at = now + self.access_token_expiry
            
            access_token = f"acc_{user.id}_{secrets.token_urlsafe(24)}"
            
            self._access_tokens[access_token] = {
                'user_id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'type': 'access',
                'created_at': now,
                'expires_at': expires_at
            }
            
            return AuthToken(
                access_token=access_token,
                refresh_token=refresh_token,  # Devolver el mismo refresh token
                expires_at=int(expires_at.timestamp())
            )
            
        except User.DoesNotExist:
            raise InvalidTokenException("Usuario no encontrado")
    
    def revoke_token(self, token: str, token_type: str = 'access'):
        """Revocar token específico"""
        if token_type == 'access':
            if token in self._access_tokens:
                del self._access_tokens[token]
        
        elif token_type == 'refresh':
            try:
                refresh_token = RefreshToken.objects.get(token=token)
                refresh_token.revoked = True
                refresh_token.save()
            except RefreshToken.DoesNotExist:
                pass
    
    def revoke_all_user_tokens(self, user_id: int):
        """Revocar todos los tokens de un usuario"""
        # Revocar access tokens en memoria
        tokens_to_remove = [
            token for token, data in self._access_tokens.items()
            if data['user_id'] == user_id
        ]
        
        for token in tokens_to_remove:
            del self._access_tokens[token]
        
        # Revocar refresh tokens en BD
        RefreshToken.objects.filter(
            user_id=user_id,
            revoked=False
        ).update(revoked=True)
    
    def get_user_active_sessions(self, user_id: int) -> list:
        """Obtener todas las sesiones activas de un usuario"""
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
        
        refresh_tokens = RefreshToken.objects.filter(
            user_id=user_id,
            revoked=False
        ).filter(expires_at__gt=timezone.now())
        
        refresh_sessions = [
            {
                'type': 'refresh',
                'token': token.token[:20] + '...',
                'created_at': token.created_at,
                'expires_at': token.expires_at,
                'id': str(token.id)
            }
            for token in refresh_tokens
        ]
        
        return access_sessions + refresh_sessions
    
    def cleanup_expired_tokens(self):
        """Limpiar tokens expirados"""
        now = timezone.now()
        
        expired_access = [
            token for token, data in self._access_tokens.items()
            if now > data['expires_at']
        ]
        
        for token in expired_access:
            del self._access_tokens[token]
        
        expired_refresh_count = RefreshToken.objects.filter(
            expires_at__lt=now
        ).count()
        
        RefreshToken.objects.filter(expires_at__lt=now).delete()
        
        return len(expired_access) + expired_refresh_count
    
    def _generate_secure_token(self, length: int = 32) -> str:
        """Generar token seguro para refresh tokens"""
        random_bytes = secrets.token_bytes(length)
        timestamp = str(timezone.now().timestamp())
        hash_input = random_bytes + timestamp.encode() + self.secret_key.encode()
        token_hash = hashlib.sha256(hash_input).digest()
        combined = random_bytes + token_hash[:16]
        token = base64.urlsafe_b64encode(combined).decode('utf-8').rstrip('=')
        return f"ref_{secrets.token_urlsafe(8)}_{token}"
