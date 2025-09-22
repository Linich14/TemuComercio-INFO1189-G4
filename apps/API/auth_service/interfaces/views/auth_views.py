from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from ...infrastructure.di.container import auth_container
from ...domain.exceptions.auth_exceptions import (
    AuthException,
    InvalidCredentialsException,
    UserNotFoundException,
    UserAlreadyExistsException,
    ValidationException,
    InactiveUserException
)
from ..serializers.auth_serializers import (
    LoginSerializer,
    RegisterSerializer,
    AuthResponseSerializer,
    RefreshTokenSerializer,
    UserProfileSerializer,
    ErrorResponseSerializer
)

class AuthViewSet(ViewSet):
    """ViewSet para operaciones de autenticación"""
    
    def get_permissions(self):
        """Define permisos según la acción"""
        if self.action in ['login', 'register', 'refresh_token']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """Endpoint para login de usuario"""
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
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
            
            # Serializar respuesta
            response_serializer = AuthResponseSerializer(auth_response.to_dict())
            
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except UserNotFoundException as e:
            return Response(
                {
                    'error': 'user_not_found',
                    'message': str(e)
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except InvalidCredentialsException as e:
            return Response(
                {
                    'error': 'invalid_credentials',
                    'message': str(e)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except InactiveUserException as e:
            return Response(
                {
                    'error': 'inactive_user',
                    'message': str(e)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except AuthException as e:
            return Response(
                {
                    'error': 'auth_error',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Endpoint para registro de usuario"""
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
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
            
            # Serializar respuesta
            response_serializer = UserProfileSerializer(user_profile.to_dict())
            
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
            
        except UserAlreadyExistsException as e:
            return Response(
                {
                    'error': 'user_already_exists',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationException as e:
            return Response(
                {
                    'error': 'validation_error',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except AuthException as e:
            return Response(
                {
                    'error': 'auth_error',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """Endpoint para renovar token de acceso"""
        serializer = RefreshTokenSerializer(data=request.data)
        
        if not serializer.is_valid():
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
            return Response(
                {
                    'error': 'auth_error',
                    'message': str(e)
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Endpoint para obtener perfil del usuario autenticado"""
        try:
            # Obtener usuario desde el token
            user_repository = auth_container.get_user_repository()
            user = user_repository.get_by_id(str(request.user.id))
            
            if not user:
                return Response(
                    {
                        'error': 'user_not_found',
                        'message': 'Usuario no encontrado'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Serializar respuesta
            response_serializer = UserProfileSerializer(user.to_dict())
            
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Endpoint para logout del usuario"""
        try:
            # Revocar todos los tokens del usuario
            token_repository = auth_container.get_token_repository()
            token_repository.revoke_all_user_tokens(str(request.user.id))
            
            return Response(
                {
                    'message': 'Sesión cerrada exitosamente'
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
