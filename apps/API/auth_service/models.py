"""
Django models for auth_service.
Infrastructure layer models.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    """Manager personalizado para el modelo de usuario"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Crea y guarda un usuario regular"""
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea y guarda un superusuario"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)

class RolUsuarioModel(models.Model):
    """Modelo para los roles de usuario"""
    rous_id = models.AutoField(primary_key=True)
    rous_nombre = models.CharField(max_length=50, unique=True)
    rous_descripcion = models.TextField(blank=True, null=True)
    rous_activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'rol_usuario'
        ordering = ['rous_id']
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'
    
    def __str__(self):
        return self.rous_nombre

class UserModel(AbstractBaseUser, PermissionsMixin):
    """Modelo unificado para usuarios"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Campos de identificación
    email = models.EmailField(unique=True, verbose_name="Email")
    rut = models.CharField(
        max_length=12, 
        unique=True, 
        null=True, 
        blank=True, 
        verbose_name="RUT"
    )
    
    # Campos de información personal
    first_name = models.CharField(max_length=50, verbose_name="Nombre")
    last_name = models.CharField(max_length=50, verbose_name="Apellido")
    
    # Campos de estado
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_staff = models.BooleanField(default=False, verbose_name="Es staff")
    
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
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Creado en")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado en")
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['rut']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    @property
    def full_name(self):
        """Retorna el nombre completo"""
        return f"{self.first_name} {self.last_name}".strip()

class RefreshToken(models.Model):
    """Modelo para tokens de refresco"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserModel, 
        on_delete=models.CASCADE, 
        related_name='refresh_tokens'
    )
    token = models.TextField(unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'auth_refresh_tokens'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['user', 'revoked']),
        ]
    
    def __str__(self):
        return f"Token for {self.user.email}"
    
    @property
    def is_valid(self):
        """Verifica si el token es válido"""
        return not self.revoked and self.expires_at > timezone.now()
