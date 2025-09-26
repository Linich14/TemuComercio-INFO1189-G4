import logging
import traceback
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ....infrastructure.di.container import auth_container
from ....domain.exceptions.auth_exceptions import (
    AuthException,
    UserAlreadyExistsException,
    ValidationException,
)
from ...serializers.auth_serializers import (
    RegisterSerializer,
    UserProfileSerializer,
)

# Configurar logger
logger = logging.getLogger('auth_service')

class RegisterAPIView(APIView):
    """Vista para registro de usuario"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Endpoint para registro de usuario"""
        logger.info(f"Intento de registro para email: {request.data.get('email', 'N/A')}")
        
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f"Datos de registro inválidos: {serializer.errors} - Email: {request.data.get('email', 'N/A')}")
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
            register_use_case = auth_container.get_register_use_case()
            user_profile = register_use_case.execute(serializer.to_dto())
            
            logger.info(f"Registro exitoso para email: {serializer.validated_data['email']}")
            
            # Serializar respuesta
            response_serializer = UserProfileSerializer(user_profile.to_dict())
            
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except UserAlreadyExistsException as e:
            logger.warning(f"Usuario ya existe en registro: {serializer.validated_data.get('email', 'N/A')} - Error: {str(e)}")
            return Response(
                {
                    'error': 'user_already_exists',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationException as e:
            logger.warning(f"Error de validación en registro: {str(e)} - Email: {serializer.validated_data.get('email', 'N/A')}")
            return Response(
                {
                    'error': 'validation_error',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except AuthException as e:
            logger.error(f"Error de autenticación en registro: {str(e)} - Email: {serializer.validated_data.get('email', 'N/A')}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return Response(
                {
                    'error': 'auth_error',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.critical(f"Error interno en registro: {str(e)} - Email: {serializer.validated_data.get('email', 'N/A')}")
            logger.critical(f"Traceback completo: {traceback.format_exc()}")
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)