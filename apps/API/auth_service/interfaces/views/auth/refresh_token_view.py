import logging
import traceback
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ....infrastructure.di.container import auth_container
from ....domain.exceptions.auth_exceptions import (
    AuthException,
)
from ...serializers.auth_serializers import (
    AuthResponseSerializer,
    RefreshTokenSerializer,
)

# Configurar logger
logger = logging.getLogger('auth_service')

class RefreshTokenAPIView(APIView):
    """Vista para renovar token de acceso"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Endpoint para renovar token de acceso"""
        refresh_token = request.data.get('refresh_token', 'N/A')[:20] + '...' if request.data.get('refresh_token') else 'N/A'
        logger.info(f"Intento de refresh token: {refresh_token}")
        
        serializer = RefreshTokenSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f"Datos de refresh token inválidos: {serializer.errors}")
            return Response(
                {
                    'error': 'validation_error',
                    'message': 'Datos inválidos',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Obtener servicio de autenticación
            auth_service = auth_container.get_auth_service()
            
            # Renovar token
            auth_token = auth_service.refresh_access_token(
                serializer.validated_data['refresh_token']
            )
            
            logger.info(f"Refresh token exitoso")
            
            # Preparar respuesta
            response_data = {
                'access_token': auth_token.access_token,
                'refresh_token': auth_token.refresh_token,
                'expires_at': auth_token.expires_at,
                'token_type': auth_token.token_type
            }
            
            response_serializer = AuthResponseSerializer(response_data)
            
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except AuthException as e:
            logger.error(f"Error de autenticación en refresh token: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response(
                {
                    'error': 'auth_error',
                    'message': str(e)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.critical(f"Error interno en refresh token: {str(e)}")
            logger.critical(f"Traceback completo: {traceback.format_exc()}")
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )