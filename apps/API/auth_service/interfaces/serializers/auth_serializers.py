from rest_framework import serializers
from ...models import UserModel, RolUsuarioModel
from ...application.dto.auth_dto import (
    UserCreateDTO, 
    LoginDTO, 
    RefreshTokenDTO, 
    RegisterRequestDTO,
    LoginRequestDTO,
    RefreshTokenRequestDTO
)

class RegisterSerializer(serializers.Serializer):
    """Serializer para registro de usuarios"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    rut = serializers.CharField(max_length=12, required=True,)
    id_role = serializers.IntegerField(required=True, allow_null=True)
    estado = serializers.BooleanField(default=True)

    def validate_email(self, value):
        """Validar que el email no esté en uso"""
        if UserModel.objects.filter(usua_email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value

    def validate_rut(self, value):
        """Validar RUT si se proporciona"""
        if value and UserModel.objects.filter(usua_rut=value).exists():
            raise serializers.ValidationError("Este RUT ya está registrado.")
        return value

    def validate_id_role(self, value):
        """Validar que el rol existe si se proporciona"""
        if value and not RolUsuarioModel.objects.filter(rous_id=value).exists():
            raise serializers.ValidationError("El rol especificado no existe.")
        return value

    def to_dto(self):
        """Convertir a DTO"""
        return RegisterRequestDTO(**self.validated_data)

class UserCreateSerializer(serializers.Serializer):
    """Serializer para crear usuarios"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    rut = serializers.CharField(max_length=12, required=False, allow_null=True, allow_blank=True)
    id_role = serializers.IntegerField(required=False, allow_null=True)
    estado = serializers.BooleanField(default=True)

    def to_dto(self):
        """Convertir a DTO"""
        return UserCreateDTO(**self.validated_data)

class UserResponseSerializer(serializers.Serializer):
    """Serializer para respuestas de usuario"""
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    estado = serializers.BooleanField(read_only=True)
    rut = serializers.CharField(read_only=True, allow_null=True)
    id_role = serializers.IntegerField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True, allow_null=True)
    updated_at = serializers.DateTimeField(read_only=True, allow_null=True)

class UserProfileSerializer(serializers.Serializer):
    """Serializer para perfil de usuario"""
    id = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    estado = serializers.BooleanField(read_only=True)
    rut = serializers.CharField(read_only=True, allow_null=True)
    id_role = serializers.IntegerField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True, allow_null=True)
    updated_at = serializers.DateTimeField(read_only=True, allow_null=True)

class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    email = serializers.EmailField()
    password = serializers.CharField()

    def to_dto(self):
        """Convertir a DTO"""
        return LoginRequestDTO(**self.validated_data)

class LoginResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de login"""
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = UserResponseSerializer()
    expires_in = serializers.IntegerField()

class AuthResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de autenticación"""
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    expires_at = serializers.IntegerField()
    token_type = serializers.CharField()
    user = UserProfileSerializer()

class RefreshTokenSerializer(serializers.Serializer):
    """Serializer para refresh token"""
    refresh_token = serializers.CharField()

    def to_dto(self):
        """Convertir a DTO"""
        return RefreshTokenRequestDTO(**self.validated_data)

class RefreshTokenResponseSerializer(serializers.Serializer):
    """Serializer para respuesta de refresh token"""
    access_token = serializers.CharField()
    expires_in = serializers.IntegerField()

class ErrorResponseSerializer(serializers.Serializer):
    """Serializer para respuestas de error"""
    error = serializers.CharField()
    message = serializers.CharField()
    details = serializers.DictField(required=False)
