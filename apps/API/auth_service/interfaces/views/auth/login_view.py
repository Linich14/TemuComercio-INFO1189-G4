import logging
import traceback
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ....infrastructure.di.container import auth_container

from ....domain.exceptions.auth_exceptions import (
    AuthException,
    InvalidCredentialsException,
    UserNotFoundException,
    InactiveUserException
)
from ...serializers.auth_serializers import (
    LoginSerializer,
    AuthResponseSerializer,
)

# Configurar logger
logger = logging.getLogger('auth_service')

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Endpoint para login de usuario"""
        logger.info(f"Intento de login para email: {request.data.get('email', 'N/A')}")
        
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f"Datos de login inválidos: {serializer.errors}")
            return Response(
                {
                    'error': 'validation_error',
                    'message': 'Datos inválidos',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Ejecutar caso de uso
            login_use_case = auth_container.get_login_use_case()
            auth_response = login_use_case.execute(serializer.to_dto())
            
            logger.info(f"Login exitoso para email: {serializer.validated_data['email']}")
            
            # Serializar respuesta
            response_serializer = AuthResponseSerializer(auth_response.to_dict())
            
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except UserNotFoundException as e:
            logger.warning(f"Usuario no encontrado en login: {serializer.validated_data.get('email', 'N/A')} - Error: {str(e)}")
            return Response(
                {
                    'error': 'user_not_found',
                    'message': str(e)
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except InvalidCredentialsException as e:
            logger.warning(f"Credenciales inválidas para email: {serializer.validated_data.get('email', 'N/A')} - Error: {str(e)}")
            return Response(
                {
                    'error': 'invalid_credentials',
                    'message': str(e)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except InactiveUserException as e:
            logger.warning(f"Usuario inactivo intentó login: {serializer.validated_data.get('email', 'N/A')} - Error: {str(e)}")
            return Response(
                {
                    'error': 'inactive_user',
                    'message': str(e)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except AuthException as e:
            logger.error(f"Error de autenticación en login: {str(e)} - Email: {serializer.validated_data.get('email', 'N/A')}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response(
                {
                    'error': 'auth_error',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.critical(f"Error interno en login: {str(e)} - Email: {serializer.validated_data.get('email', 'N/A')}")
            logger.critical(f"Traceback completo: {traceback.format_exc()}")
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
