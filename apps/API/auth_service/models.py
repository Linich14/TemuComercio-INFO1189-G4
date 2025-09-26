"""
Django models for auth_service.
Infrastructure layer models.
"""
from django.db import models
from django.utils import timezone
import uuid

class RolUsuarioModel(models.Model):
    """Modelo para los roles de usuario"""
    rous_id = models.AutoField(primary_key=True)
    rous_nombre = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'rol_usuario'
        ordering = ['rous_id']
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'
    
    def __str__(self):
        return self.rous_nombre

class UserModel(models.Model):
    """Modelo unificado para usuarios"""
    usua_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Campos de identificación
    usua_email = models.EmailField(unique=True, verbose_name="Email")
    usua_rut = models.CharField(
        max_length=12, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name="RUT"
    )
    usua_pass = models.CharField(max_length=128, verbose_name="Contraseña")
    usua_estado = models.BooleanField(default=True, verbose_name="Estado")
    
    # Campos de relaciones
    rous_id = models.ForeignKey(
        RolUsuarioModel, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name="usuarios", 
        verbose_name="Rol de usuario"
    )
    
    # Campos de timestamps
    usua_creado = models.DateTimeField(default=timezone.now, verbose_name="Creado en")
    usua_actualizado = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")
    
    # Campos requeridos por AbstractBaseUser y PermissionsMixin    
    password = None
    last_login = None
    is_superuser = None

    USERNAME_FIELD = 'usua_email'
    REQUIRED_FIELDS = ['usua_rut']
    
    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        indexes = [
            models.Index(fields=['usua_email']),
            models.Index(fields=['usua_rut']),
        ]
    
class RefreshToken(models.Model):
    """Modelo para tokens de refresco"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usua_id = models.ForeignKey(
        UserModel, 
        on_delete=models.CASCADE, 
        related_name='refresh_tokens'
    )
    token_valor = models.TextField(unique=True)
    token_expira_en = models.DateTimeField()
    token_creado_en = models.DateTimeField(auto_now_add=True)
    token_activo = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Session_token'
        indexes = [
            models.Index(fields=['token_valor']),
            models.Index(fields=['token_expira_en']),
            models.Index(fields=['usua_id', 'token_activo']),
        ]
    
    def __str__(self):
        return f"Token for {self.usua_id.usua_email}"
    
    @property
    def is_valid(self):
        """Verifica si el token es válido"""
        return not self.token_activo and self.token_expira_en > timezone.now()
