class AuthenticationException(Exception):
    """Excepción base para errores de autenticación"""
    pass

class InvalidCredentialsException(AuthenticationException):
    """Credenciales inválidas"""
    pass

class UserAlreadyExistsException(Exception):
    """Usuario ya existe"""
    pass

class AccountNotVerifiedException(AuthenticationException):
    """Cuenta no verificada"""
    pass

class TokenExpiredException(AuthenticationException):
    """Token expirado"""
    pass

class InvalidTokenException(AuthenticationException):
    """Token inválido"""
    pass

class UserNotFoundException(AuthenticationException):
    pass
