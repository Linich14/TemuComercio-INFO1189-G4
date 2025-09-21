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
