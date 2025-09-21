# interfaces/api/auth_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging

from ..serializers.auth_serializers import LoginSerializer, RegisterSerializer
from ....core.application.dto.auth_dto import LoginRequestDTO, RegisterRequestDTO
from ....core.domain.exceptions.auth_exceptions import *
from ....infrastructure.di.container import get_container

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    """API endpoint para login de usuarios"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            login_dto = LoginRequestDTO(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            container = get_container()
            login_use_case = container.get_login_use_case()
            
            result = login_use_case.execute(login_dto)
            
            return Response({
                'message': 'Login exitoso',
                'data': {
                    'access_token': result.access_token,
                    'refresh_token': result.refresh_token,
                    'expires_at': result.expires_at,
                    'user': {
                        'id': result.user.id,
                        'email': result.user.email,
                        'first_name': result.user.first_name,
                        'last_name': result.user.last_name
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except InvalidCredentialsException as e:
            logger.warning(f"Intento de login fallido: {str(e)}")
            return Response({
                'error': 'Credenciales inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        except UserNotFoundException as e:
            logger.warning(f"Usuario no encontrado en login: {str(e)}")
            return Response({
                'error': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            logger.error(f"Error interno en login: {str(e)}")
            return Response({
                'error': 'Error interno del servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterAPIView(APIView):
    """API endpoint para registro de usuarios"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # 1. Validar datos de entrada
            serializer = RegisterSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'error': 'Datos inválidos',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 2. Crear DTO
            register_dto = RegisterRequestDTO(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                phone=serializer.validated_data.get('phone'),
                rut=serializer.validated_data.get('rut'),
                birth_date=serializer.validated_data.get('birth_date')
            )
            
            # 3. Ejecutar caso de uso
            container = get_container()
            register_use_case = container.register_use_case()
            
            result = register_use_case.execute(register_dto)
            
            # 4. Retornar respuesta
            return Response({
                'message': 'Usuario registrado exitosamente',
                'data': {
                    'user': {
                        'id': result.user.id,
                        'email': result.user.email,
                        'first_name': result.user.first_name,
                        'last_name': result.user.last_name
                    }
                }
            }, status=status.HTTP_201_CREATED)
            
        except UserAlreadyExistsException as e:
            return Response({
                'error': 'El usuario ya existe'
            }, status=status.HTTP_409_CONFLICT)
            
        except Exception as e:
            logger.error(f"Error en registro: {str(e)}")
            return Response({
                'error': 'Error interno del servidor'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)