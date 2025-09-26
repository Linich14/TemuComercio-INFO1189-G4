from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import AnonymousUser
from ...infrastructure.di.container import auth_container
import logging

logger = logging.getLogger('auth_service')

class CustomTokenAuthentication(BaseAuthentication):
    """
    Autenticación personalizada usando nuestro servicio de auth
    """
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if not auth_header:
            return None
            
        try:
            # Extraer token del header
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return None
                
            token = parts[1]
            
            # Validar token usando nuestro servicio
            auth_service = auth_container.get_auth_service()
            user_id = auth_service.validate_access_token(token)
            
            if not user_id:
                raise AuthenticationFailed('Token inválido')
            
            # Obtener usuario
            user_repository = auth_container.get_user_repository()
            user = user_repository.get_by_id(user_id)
            
            if not user:
                raise AuthenticationFailed('Usuario no encontrado')
                
            if not user.estado:
                raise AuthenticationFailed('Usuario inactivo')
            
            # Crear un objeto user simple para DRF
            class AuthenticatedUser:
                def __init__(self, user_data):
                    self.id = user_data.id
                    self.email = user_data.email
                    self.is_authenticated = True
                    # Corregir: usar estado en lugar de is_active
                    self.is_active = user_data.estado
                    
            return (AuthenticatedUser(user), token)
            
        except AuthenticationFailed:
            # Re-lanzar excepciones de autenticación
            raise
        except Exception as e:
            logger.warning(f"Error en autenticación: {str(e)}")
            raise AuthenticationFailed('Error de autenticación')

    def authenticate_header(self, request):
        return 'Bearer'