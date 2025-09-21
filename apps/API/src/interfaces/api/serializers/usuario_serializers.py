"""
Usuario serializers - API interface layer
Django REST Framework serializers for Usuario API.
"""
from rest_framework import serializers
from datetime import datetime


class CreateUsuarioSerializer(serializers.Serializer):
    """Serializer for creating a new Usuario."""
    
    usua_rut = serializers.CharField(
        max_length=25,
        help_text="RUT del usuario (formato: 12.345.678-9)"
    )
    usua_email = serializers.EmailField(
        max_length=200,
        help_text="Email del usuario"
    )
    usua_pass = serializers.CharField(
        max_length=128,
        write_only=True,
        style={'input_type': 'password'},
        help_text="Contraseña del usuario"
    )
    rous_id = serializers.IntegerField(
        default=4,
        help_text="ID del rol (1=Administrador, 2=Municipal, 3=Fiscalizador, 4=Usuario)"
    )
    
    def validate_usua_rut(self, value):
        """Validate RUT format."""
        # Remove dots and hyphens for validation
        clean_rut = value.replace(".", "").replace("-", "")
        if len(clean_rut) < 8:
            raise serializers.ValidationError("RUT debe tener al menos 8 caracteres")
        return value
    
    def validate_rous_id(self, value):
        """Validate role ID."""
        if value not in [1, 2, 3, 4]:
            raise serializers.ValidationError("Rol inválido. Debe ser 1, 2, 3 o 4")
        return value


class UpdateUsuarioSerializer(serializers.Serializer):
    """Serializer for updating a Usuario."""
    
    usua_rut = serializers.CharField(
        max_length=25,
        required=False,
        help_text="RUT del usuario"
    )
    usua_email = serializers.EmailField(
        max_length=200,
        required=False,
        help_text="Email del usuario"
    )
    usua_pass = serializers.CharField(
        max_length=128,
        required=False,
        write_only=True,
        style={'input_type': 'password'},
        help_text="Nueva contraseña del usuario"
    )
    rous_id = serializers.IntegerField(
        required=False,
        help_text="ID del rol"
    )
    usua_estado = serializers.IntegerField(
        required=False,
        help_text="Estado del usuario (0=Deshabilitado, 1=Habilitado)"
    )
    
    def validate_usua_rut(self, value):
        """Validate RUT format."""
        if value:
            clean_rut = value.replace(".", "").replace("-", "")
            if len(clean_rut) < 8:
                raise serializers.ValidationError("RUT debe tener al menos 8 caracteres")
        return value
    
    def validate_rous_id(self, value):
        """Validate role ID."""
        if value is not None and value not in [1, 2, 3, 4]:
            raise serializers.ValidationError("Rol inválido. Debe ser 1, 2, 3 o 4")
        return value
    
    def validate_usua_estado(self, value):
        """Validate user status."""
        if value is not None and value not in [0, 1]:
            raise serializers.ValidationError("Estado inválido. Debe ser 0 o 1")
        return value


class UsuarioResponseSerializer(serializers.Serializer):
    """Serializer for Usuario response."""
    
    usua_id = serializers.IntegerField(read_only=True)
    usua_rut = serializers.CharField(read_only=True)
    usua_email = serializers.EmailField(read_only=True)
    usua_creado = serializers.DateTimeField(read_only=True)
    usua_actualizado = serializers.DateTimeField(read_only=True, allow_null=True)
    usua_estado = serializers.IntegerField(read_only=True)
    rous_id = serializers.IntegerField(read_only=True)
    rol_nombre = serializers.CharField(read_only=True, allow_null=True)
    
    def to_representation(self, instance):
        """Custom representation with role name mapping."""
        data = super().to_representation(instance)
        
        # Map role ID to role name
        role_names = {
            1: "Administrador",
            2: "Municipal", 
            3: "Fiscalizador",
            4: "Usuario"
        }
        
        if 'rous_id' in data and data['rous_id']:
            data['rol_nombre'] = role_names.get(data['rous_id'], "Desconocido")
        
        # Format estado as string for better readability
        if 'usua_estado' in data:
            data['usua_estado_texto'] = "Habilitado" if data['usua_estado'] == 1 else "Deshabilitado"
        
        return data


class UsuarioListSerializer(serializers.Serializer):
    """Serializer for Usuario list response."""
    
    usuarios = UsuarioResponseSerializer(many=True, read_only=True)
    total = serializers.IntegerField(read_only=True)


class UsuarioStatusSerializer(serializers.Serializer):
    """Serializer for changing Usuario status."""
    
    usua_estado = serializers.IntegerField(
        help_text="Estado del usuario (0=Deshabilitado, 1=Habilitado)"
    )
    
    def validate_usua_estado(self, value):
        """Validate user status."""
        if value not in [0, 1]:
            raise serializers.ValidationError("Estado inválido. Debe ser 0 o 1")
        return value