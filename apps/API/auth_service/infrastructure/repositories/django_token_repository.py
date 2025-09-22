from typing import Optional
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ...models import RefreshToken, UserModel
from ...domain.repositories.token_repository import TokenRepositoryInterface

class DjangoTokenRepository(TokenRepositoryInterface):
    """Implementación Django del repositorio de tokens"""
    
    def save_refresh_token(self, user_id: str, token: str, expires_at: datetime) -> bool:
        """Guarda un refresh token"""
        try:
            user = UserModel.objects.get(id=user_id)
            
            # Revocar tokens anteriores del usuario (opcional)
            RefreshToken.objects.filter(user=user, revoked=False).update(revoked=True)
            
            # Crear nuevo token
            RefreshToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )
            return True
        except ObjectDoesNotExist:
            return False
        except Exception:
            return False
    
    def get_refresh_token(self, token: str) -> Optional[dict]:
        """Obtiene información de un refresh token"""
        try:
            refresh_token = RefreshToken.objects.get(token=token)
            
            # Verificar si el token es válido
            is_valid = refresh_token.is_valid
            
            return {
                'user_id': str(refresh_token.user.id),
                'token': refresh_token.token,
                'expires_at': refresh_token.expires_at,
                'is_valid': is_valid,
                'revoked': refresh_token.revoked,
                'created_at': refresh_token.created_at
            }
        except ObjectDoesNotExist:
            return None
    
    def revoke_refresh_token(self, token: str) -> bool:
        """Revoca un refresh token"""
        try:
            refresh_token = RefreshToken.objects.get(token=token)
            refresh_token.revoked = True
            refresh_token.save()
            return True
        except ObjectDoesNotExist:
            return False
    
    def revoke_all_user_tokens(self, user_id: str) -> bool:
        """Revoca todos los tokens de un usuario"""
        try:
            RefreshToken.objects.filter(
                user_id=user_id,
                revoked=False
            ).update(revoked=True)
            return True
        except Exception:
            return False
    
    def clean_expired_tokens(self) -> int:
        """Limpia tokens expirados"""
        now = timezone.now()
        
        # Obtener count antes de eliminar
        expired_tokens = RefreshToken.objects.filter(expires_at__lt=now)
        count = expired_tokens.count()
        
        # Eliminar tokens expirados
        expired_tokens.delete()
        
        return count
    
    def get_user_refresh_tokens(self, user_id: str, active_only: bool = True) -> list:
        """Obtiene todos los refresh tokens de un usuario"""
        queryset = RefreshToken.objects.filter(user_id=user_id)
        
        if active_only:
            queryset = queryset.filter(
                revoked=False,
                expires_at__gt=timezone.now()
            )
        
        return [
            {
                'token': token.token[:20] + '...',
                'created_at': token.created_at,
                'expires_at': token.expires_at,
                'revoked': token.revoked,
                'is_valid': token.is_valid,
                'id': str(token.id)
            }
            for token in queryset
        ]
