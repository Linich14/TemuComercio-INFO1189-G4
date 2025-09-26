import logging
import traceback
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from ....infrastructure.di.container import auth_container
from ....interfaces.Authentication.CustomAuthentication import CustomTokenAuthentication

logger = logging.getLogger('auth_service')

class LogoutAPIView(APIView):
    """Vista para logout del usuario"""
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Endpoint para logout del usuario"""
        user_id = getattr(request.user, 'id', 'N/A')
        logger.info(f"Intento de logout para usuario ID: {user_id}")
        
        try:
            # Revocar todos los tokens del usuario
            token_repository = auth_container.get_token_repository()
            token_repository.revoke_all_user_tokens(str(request.user.id))
            
            logger.info(f"Logout exitoso para usuario ID: {user_id}")
            
            return Response(
                {
                    'message': 'Sesión cerrada exitosamente'
                },
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            logger.critical(f"Error interno en logout: {str(e)} - Usuario ID: {user_id}")
            logger.critical(f"Traceback completo: {traceback.format_exc()}")
            return Response(
                {
                    'error': 'internal_error',
                    'message': 'Error interno del servidor'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
