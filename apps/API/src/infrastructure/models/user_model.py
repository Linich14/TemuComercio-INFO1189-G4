# infrastructure/models/user_models.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils import timezone
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Campos personalizados
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name='Email')
    rut = models.CharField(unique=True, max_length=12, blank=True, null=True, verbose_name='RUT')
    first_name = models.CharField(max_length=50, verbose_name='Nombre')
    last_name = models.CharField(max_length=50, verbose_name='Apellido')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Teléfono')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')
    avatar = models.URLField(blank=True, null=True, verbose_name='Avatar')
    
    # Campos de control
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_staff = models.BooleanField(default=False, verbose_name='Es staff')
    is_verified = models.BooleanField(default=False, verbose_name='Email verificado')
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado en')
    last_login_at = models.DateTimeField(blank=True, null=True, verbose_name='Último login')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', "rut"]
    
    class Meta:
        app_label = 'auth_service'
        db_table = 'auth_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()