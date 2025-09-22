from typing import Dict, Any
from ...domain.repositories.user_repository import UserRepositoryInterface
from ...domain.repositories.token_repository import TokenRepositoryInterface
from ...domain.services.auth_service import AuthServiceInterface
from ...domain.services.password_service import PasswordServiceInterface
from ...domain.services.validation_service import ValidationServiceInterface
from ...application.use_cases.login_use_case import LoginUseCase
from ...application.use_cases.register_use_case import RegisterUseCase
from ..repositories.django_user_repository import DjangoUserRepository
from ..repositories.django_token_repository import DjangoTokenRepository
from ..services.django_auth_service import DjangoAuthService
from ..services.django_password_service import DjangoPasswordService
from ..services.validation_service import ValidationService

class AuthContainer:
    """Contenedor de dependencias para el módulo de autenticación"""
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        """Configura todas las dependencias"""
        # Repositories
        self._services['user_repository'] = DjangoUserRepository()
        self._services['token_repository'] = DjangoTokenRepository()
        
        # Services
        self._services['password_service'] = DjangoPasswordService()
        self._services['validation_service'] = ValidationService()
        
        # Auth service que usa el token repository
        self._services['auth_service'] = DjangoAuthService(
            self._services['token_repository']
        )
        
        # Use Cases
        self._services['login_use_case'] = LoginUseCase(
            self._services['user_repository'],
            self._services['auth_service'],
            self._services['password_service']
        )
        
        self._services['register_use_case'] = RegisterUseCase(
            self._services['user_repository'],
            self._services['password_service'],
            self._services['validation_service']
        )
    
    def get_user_repository(self) -> UserRepositoryInterface:
        """Obtiene el repositorio de usuarios"""
        return self._services['user_repository']
    
    def get_token_repository(self) -> TokenRepositoryInterface:
        """Obtiene el repositorio de tokens"""
        return self._services['token_repository']
    
    def get_auth_service(self) -> AuthServiceInterface:
        """Obtiene el servicio de autenticación"""
        return self._services['auth_service']
    
    def get_password_service(self) -> PasswordServiceInterface:
        """Obtiene el servicio de contraseñas"""
        return self._services['password_service']
    
    def get_validation_service(self) -> ValidationServiceInterface:
        """Obtiene el servicio de validación"""
        return self._services['validation_service']
    
    def get_login_use_case(self) -> LoginUseCase:
        """Obtiene el caso de uso de login"""
        return self._services['login_use_case']
    
    def get_register_use_case(self) -> RegisterUseCase:
        """Obtiene el caso de uso de registro"""
        return self._services['register_use_case']

# Instancia global del contenedor
auth_container = AuthContainer()
