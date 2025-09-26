import logging
import traceback
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ....infrastructure.di.container import auth_container

from ...serializers.auth_serializers import (
    UserProfileSerializer,
)
from ....interfaces.Authentication.CustomAuthentication import CustomTokenAuthentication

# Configurar logger
logger = logging.getLogger('auth_service')

class ProfileAPIView(APIView):
    """Vista para obtener perfil del usuario autenticado"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Endpoint para obtener perfil del usuario autenticado"""
        user_id = getattr(request.user, 'id', 'N/A')
        logger.info(f"Solicitud de perfil para usuario ID: {user_id}")
        
        try:
            # Obtener usuario desde el token
            user_repository = auth_container.get_user_repository()
            user = user_repository.get_by_id(str(request.user.id))
            
            if not user:
                logger.warning(f"Usuario no encontrado en solicitud de perfil - ID: {user_id}")
                return Response(
                    {
                        'error': 'user_not_found',
                        'message': 'Usuario no encontrado'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            logger.info(f"Perfil obtenido exitosamente para usuario ID: {user_id}")
            
            # Serializar respuesta
            response_serializer = UserProfileSerializer(user.to_dict())
            
            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.critical(f"Error interno en obtener perfil: {str(e)} - Usuario ID: {user_id}")
            logger.critical(f"Traceback completo: {traceback.format_exc()}")
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
