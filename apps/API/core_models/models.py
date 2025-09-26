"""
Django models for the core infrastructure layer.
Maps domain entities to database tables following Clean Architecture.
"""
from django.db import models


class RolUsuarioModel(models.Model):
    """
    Django model for RolUsuario entity.
    Infrastructure concern - database representation.
    """
    
    rous_id = models.AutoField(primary_key=True)
    rous_nombre = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'rol_usuario'
        verbose_name = 'Rol de Usuario'
        verbose_name_plural = 'Roles de Usuario'
        ordering = ['rous_id']
    
    def __str__(self):
        return self.rous_nombre


class UsuarioModel(models.Model):
    """
    Django model for Usuario entity.
    Infrastructure concern - database representation.
    """
    
    usua_id = models.IntegerField(primary_key=True)  # Random ID will be set in save()
    usua_rut = models.CharField(max_length=25, unique=True)
    usua_email = models.EmailField(max_length=200, unique=True)
    usua_pass = models.CharField(max_length=128)  # Hashed password
    usua_creado = models.DateTimeField(auto_now_add=True)
    usua_actualizado = models.DateTimeField(null=True, blank=True)
    usua_estado = models.IntegerField(
        default=1,
        choices=[(0, 'Deshabilitado'), (1, 'Habilitado')]
    )
    rous_id = models.ForeignKey(
        RolUsuarioModel,
        on_delete=models.PROTECT,  # Protect role deletion if users exist
        db_column='rous_id'
    )
    
    class Meta:
        db_table = 'Usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-usua_creado']
    
    def save(self, *args, **kwargs):
        """Generate random ID if not set."""
        if not self.usua_id:
            import random
            self.usua_id = random.randint(100000, 999999)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.usua_email} ({self.usua_rut})"


class SesionTokenModel(models.Model):
    """
    Django model for SesionToken entity.
    Infrastructure concern - database representation.
    """
    
    token_id = models.AutoField(primary_key=True)
    usua_id = models.ForeignKey(
        UsuarioModel,
        on_delete=models.CASCADE,
        db_column='usua_id'
    )
    token_valor = models.CharField(max_length=36, unique=True)  # UUID
    token_creado_en = models.DateTimeField(auto_now_add=True)
    token_expira_en = models.DateTimeField()
    token_activo = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'Sesion_Token'
        verbose_name = 'Token de Sesión'
        verbose_name_plural = 'Tokens de Sesión'
        ordering = ['-token_creado_en']
        indexes = [
            models.Index(fields=['token_valor']),
            models.Index(fields=['usua_id', 'token_activo']),
        ]
    
    def __str__(self):
        return f"Token {self.token_valor[:8]}... para {self.usua_id.usua_email}"
    
    @property
    def is_expired(self):
        """Verifica si el token ha expirado"""
        from django.utils import timezone
        return timezone.now() > self.token_expira_en
