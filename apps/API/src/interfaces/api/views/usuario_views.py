"""
Usuario API views - Interface layer
Django REST Framework views for Usuario API endpoints.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import Http404

from ..serializers.usuario_serializers import (
    CreateUsuarioSerializer,
    UpdateUsuarioSerializer,
    UsuarioResponseSerializer,
    UsuarioListSerializer,
    UsuarioStatusSerializer
)
from ....core.application.dto.usuario_dto import CreateUsuarioDTO, UpdateUsuarioDTO
from ....core.application.use_cases.usuario_use_cases import (
    CreateUsuarioUseCase,
    GetUsuarioUseCase,
    UpdateUsuarioUseCase,
    ListUsuariosUseCase,
    DisableUsuarioUseCase,
    EnableUsuarioUseCase
)
from ..dependencies import get_usuario_repository


@api_view(['POST'])
@permission_classes([AllowAny])  # TODO: Add proper authentication
def create_usuario(request):
    """
    Create a new Usuario.
    
    POST /api/usuarios/
    """
    try:
        # Validate input
        serializer = CreateUsuarioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Validation failed',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create DTO
        dto = CreateUsuarioDTO(
            usua_rut=serializer.validated_data['usua_rut'],
            usua_email=serializer.validated_data['usua_email'],
            usua_pass=serializer.validated_data['usua_pass'],
            rous_id=serializer.validated_data.get('rous_id', 4)
        )
        
        # Execute use case
        use_case = CreateUsuarioUseCase(get_usuario_repository())
        result = use_case.execute(dto)
        
        # Serialize response
        response_serializer = UsuarioResponseSerializer(result)
        
        return Response(
            {
                'message': 'Usuario created successfully',
                'data': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        
    except ValueError as e:
        return Response(
            {
                'error': 'Validation error',
                'message': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {
                'error': 'Internal server error',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: Add proper authentication
def get_usuario(request, usua_id):
    """
    Get Usuario by ID.
    
    GET /api/usuarios/{usua_id}/
    """
    try:
        use_case = GetUsuarioUseCase(get_usuario_repository())
        result = use_case.execute(usua_id)
        
        if not result:
            return Response(
                {
                    'error': 'Not found',
                    'message': f'Usuario with ID {usua_id} not found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Serialize response
        response_serializer = UsuarioResponseSerializer(result)
        
        return Response(
            {
                'data': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {
                'error': 'Internal server error',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])  # TODO: Add proper authentication
def list_usuarios(request):
    """
    List all Usuarios.
    
    GET /api/usuarios/
    """
    try:
        # Get query parameters
        active_only = request.GET.get('active_only', 'true').lower() == 'true'
        
        # Execute use case
        use_case = ListUsuariosUseCase(get_usuario_repository())
        results = use_case.execute(active_only)
        
        # Serialize response
        response_data = {
            'usuarios': results,
            'total': len(results)
        }
        response_serializer = UsuarioListSerializer(response_data)
        
        return Response(
            {
                'data': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {
                'error': 'Internal server error',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([AllowAny])  # TODO: Add proper authentication
def update_usuario(request, usua_id):
    """
    Update Usuario.
    
    PUT /api/usuarios/{usua_id}/
    """
    try:
        # Validate input
        serializer = UpdateUsuarioSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'Validation failed',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create DTO
        dto = UpdateUsuarioDTO(
            usua_id=usua_id,
            usua_rut=serializer.validated_data.get('usua_rut'),
            usua_email=serializer.validated_data.get('usua_email'),
            usua_pass=serializer.validated_data.get('usua_pass'),
            rous_id=serializer.validated_data.get('rous_id'),
            usua_estado=serializer.validated_data.get('usua_estado')
        )
        
        # Execute use case
        use_case = UpdateUsuarioUseCase(get_usuario_repository())
        result = use_case.execute(dto)
        
        # Serialize response
        response_serializer = UsuarioResponseSerializer(result)
        
        return Response(
            {
                'message': 'Usuario updated successfully',
                'data': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    except ValueError as e:
        return Response(
            {
                'error': 'Validation error',
                'message': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {
                'error': 'Internal server error',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PATCH'])
@permission_classes([AllowAny])  # TODO: Add proper authentication
def disable_usuario(request, usua_id):
    """
    Disable Usuario.
    
    PATCH /api/usuarios/{usua_id}/disable/
    """
    try:
        use_case = DisableUsuarioUseCase(get_usuario_repository())
        result = use_case.execute(usua_id)
        
        # Serialize response
        response_serializer = UsuarioResponseSerializer(result)
        
        return Response(
            {
                'message': 'Usuario disabled successfully',
                'data': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    except ValueError as e:
        return Response(
            {
                'error': 'Validation error',
                'message': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {
                'error': 'Internal server error',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PATCH'])
@permission_classes([AllowAny])  # TODO: Add proper authentication
def enable_usuario(request, usua_id):
    """
    Enable Usuario.
    
    PATCH /api/usuarios/{usua_id}/enable/
    """
    try:
        use_case = EnableUsuarioUseCase(get_usuario_repository())
        result = use_case.execute(usua_id)
        
        # Serialize response
        response_serializer = UsuarioResponseSerializer(result)
        
        return Response(
            {
                'message': 'Usuario enabled successfully',
                'data': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
        
    except ValueError as e:
        return Response(
            {
                'error': 'Validation error',
                'message': str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {
                'error': 'Internal server error',
                'message': str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )