from rest_framework import serializers
from ...application.dto.auth_dto import (
    LoginRequestDTO,
    RegisterRequestDTO,
    AuthResponseDTO,
    RefreshTokenRequestDTO,
    UserProfileDTO
)

class LoginSerializer(serializers.Serializer):
    """Serializer para login de usuario"""
    email = serializers.EmailField(
        max_length=254,
        help_text="Email del usuario"
    )
    password = serializers.CharField(
        max_length=128,
        write_only=True,
        help_text="Contraseña del usuario"
    )
    
    def validate_email(self, value):
        """Valida y normaliza el email"""
        return value.lower().strip()
    
    def to_dto(self) -> LoginRequestDTO:
        """Convierte a DTO del dominio"""
        return LoginRequestDTO(
            email=self.validated_data['email'],
            password=self.validated_data['password']
        )

class RegisterSerializer(serializers.Serializer):
    """Serializer para registro de usuario"""
    email = serializers.EmailField(
        max_length=254,
        help_text="Email del usuario"
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        help_text="Contraseña del usuario (mínimo 8 caracteres)"
    )
    confirm_password = serializers.CharField(
        max_length=128,
        write_only=True,
        help_text="Confirmación de contraseña"
    )
    first_name = serializers.CharField(
        max_length=50,
        help_text="Nombre del usuario"
    )
    last_name = serializers.CharField(
        max_length=50,
        help_text="Apellido del usuario"
    )
    rut = serializers.CharField(
        max_length=12,
        required=False,
        allow_blank=True,
        help_text="RUT del usuario (opcional)"
    )
    id_role = serializers.IntegerField(
        required=False,
        help_text="ID del rol del usuario (opcional, por defecto 4)"
    )
    
    def validate_email(self, value):
        """Valida y normaliza el email"""
        return value.lower().strip()
    
    def validate_first_name(self, value):
        """Valida y normaliza el nombre"""
        return value.strip().title()
    
    def validate_last_name(self, value):
        """Valida y normaliza el apellido"""
        return value.strip().title()
    
    def validate_rut(self, value):
        """Valida y normaliza el RUT"""
        if value:
            return value.replace(".", "").replace("-", "").upper().strip()
        return value
    
    def validate(self, attrs):
        """Validación cruzada"""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        
        # Remover confirm_password ya que no lo necesitamos en el DTO
        attrs.pop('confirm_password')
        return attrs
    
    def to_dto(self) -> RegisterRequestDTO:
        """Convierte a DTO del dominio"""
        return RegisterRequestDTO(
            email=self.validated_data['email'],
            password=self.validated_data['password'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            rut=self.validated_data.get('rut'),
            id_role=self.validated_data.get('id_role')
        )

class UserProfileSerializer(serializers.Serializer):
    """Serializer para perfil de usuario"""
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    rut = serializers.CharField(read_only=True, allow_null=True)
    id_role = serializers.IntegerField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)

class AuthResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de autenticación"""
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    expires_at = serializers.IntegerField(read_only=True)
    token_type = serializers.CharField(read_only=True)
    user = UserProfileSerializer(read_only=True)

class RefreshTokenSerializer(serializers.Serializer):
    """Serializer para refresh token"""
    refresh_token = serializers.CharField(
        help_text="Refresh token para renovar el acceso"
    )
    
    def to_dto(self) -> RefreshTokenRequestDTO:
        """Convierte a DTO del dominio"""
        return RefreshTokenRequestDTO(
            refresh_token=self.validated_data['refresh_token']
        )

class ErrorResponseSerializer(serializers.Serializer):
    """Serializer para respuestas de error"""
    error = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    details = serializers.DictField(read_only=True, required=False)
