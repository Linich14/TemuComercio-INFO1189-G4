class AuthException(Exception):
    """Excepción base para errores de autenticación"""
    def __init__(self, message: str = "Error de autenticación"):
        self.message = message
        super().__init__(self.message)

class InvalidCredentialsException(AuthException):
    """Excepción para credenciales inválidas"""
    def __init__(self, message: str = "Credenciales inválidas"):
        super().__init__(message)

class UserNotFoundException(AuthException):
    """Excepción para usuario no encontrado"""
    def __init__(self, message: str = "Usuario no encontrado"):
        super().__init__(message)

class UserAlreadyExistsException(AuthException):
    """Excepción para usuario ya existente"""
    def __init__(self, message: str = "El usuario ya existe"):
        super().__init__(message)

class TokenExpiredException(AuthException):
    """Excepción para token expirado"""
    def __init__(self, message: str = "Token expirado"):
        super().__init__(message)

class InvalidTokenException(AuthException):
    """Excepción para token inválido"""
    def __init__(self, message: str = "Token inválido"):
        super().__init__(message)

class InactiveUserException(AuthException):
    """Excepción para usuario inactivo"""
    def __init__(self, message: str = "Usuario inactivo"):
        super().__init__(message)

class ValidationException(AuthException):
    """Excepción para errores de validación"""
    def __init__(self, message: str = "Error de validación"):
        super().__init__(message)
