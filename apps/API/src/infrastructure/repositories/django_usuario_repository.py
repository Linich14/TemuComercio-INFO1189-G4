"""
Django implementation of Usuario repository.
Infrastructure layer - adapts Django ORM to domain interface.
"""
from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction

from ...core.domain.entities.usuario import Usuario
from ...core.domain.repositories.usuario_repository import UsuarioRepository
from core_models.models import UsuarioModel, RolUsuarioModel
from .base_repository import RepositoryError


class DjangoUsuarioRepository(UsuarioRepository):
    """
    Django ORM implementation of UsuarioRepository.
    Follows Adapter pattern to translate between domain and infrastructure.
    """
    
    def _model_to_entity(self, model: UsuarioModel) -> Usuario:
        """Convert Django model to domain entity."""
        return Usuario(
            usua_id=model.usua_id,
            usua_rut=model.usua_rut,
            usua_email=model.usua_email,
            usua_pass=model.usua_pass,
            usua_creado=model.usua_creado,
            usua_actualizado=model.usua_actualizado,
            usua_estado=model.usua_estado,
            rous_id=model.rous_id.rous_id if model.rous_id else None
        )
    
    def _entity_to_model(self, entity: Usuario, model: Optional[UsuarioModel] = None) -> UsuarioModel:
        """Convert domain entity to Django model."""
        if model is None:
            model = UsuarioModel()
        
        if entity.usua_id:
            model.usua_id = entity.usua_id
        model.usua_rut = entity.usua_rut
        model.usua_email = entity.usua_email
        model.usua_pass = entity.usua_pass
        model.usua_creado = entity.usua_creado
        model.usua_actualizado = entity.usua_actualizado
        model.usua_estado = entity.usua_estado
        
        # Handle foreign key relationship
        if entity.rous_id:
            try:
                model.rous_id = RolUsuarioModel.objects.get(rous_id=entity.rous_id)
            except ObjectDoesNotExist:
                raise RepositoryError(f"Role with ID {entity.rous_id} not found")
        
        return model
    
    def create(self, usuario: Usuario) -> Usuario:
        """Create a new usuario."""
        try:
            with transaction.atomic():
                model = self._entity_to_model(usuario)
                model.save()
                return self._model_to_entity(model)
        except IntegrityError as e:
            if 'usua_email' in str(e):
                raise RepositoryError(f"Email {usuario.usua_email} already exists")
            elif 'usua_rut' in str(e):
                raise RepositoryError(f"RUT {usuario.usua_rut} already exists")
            else:
                raise RepositoryError(f"Error creating usuario: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error creating usuario: {str(e)}")
    
    def get_by_id(self, usua_id: int) -> Optional[Usuario]:
        """Get usuario by ID."""
        try:
            model = UsuarioModel.objects.select_related('rous_id').get(usua_id=usua_id)
            return self._model_to_entity(model)
        except ObjectDoesNotExist:
            return None
    
    def get_by_email(self, usua_email: str) -> Optional[Usuario]:
        """Get usuario by email."""
        try:
            model = UsuarioModel.objects.select_related('rous_id').get(usua_email=usua_email)
            return self._model_to_entity(model)
        except ObjectDoesNotExist:
            return None
    
    def get_by_rut(self, usua_rut: str) -> Optional[Usuario]:
        """Get usuario by RUT."""
        try:
            model = UsuarioModel.objects.select_related('rous_id').get(usua_rut=usua_rut)
            return self._model_to_entity(model)
        except ObjectDoesNotExist:
            return None
    
    def update(self, usuario: Usuario) -> Usuario:
        """Update an existing usuario."""
        try:
            with transaction.atomic():
                model = UsuarioModel.objects.select_related('rous_id').get(usua_id=usuario.usua_id)
                model = self._entity_to_model(usuario, model)
                model.save()
                return self._model_to_entity(model)
        except ObjectDoesNotExist:
            raise RepositoryError(f"Usuario with ID {usuario.usua_id} not found")
        except IntegrityError as e:
            if 'usua_email' in str(e):
                raise RepositoryError(f"Email {usuario.usua_email} already exists")
            elif 'usua_rut' in str(e):
                raise RepositoryError(f"RUT {usuario.usua_rut} already exists")
            else:
                raise RepositoryError(f"Error updating usuario: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error updating usuario: {str(e)}")
    
    def delete(self, usua_id: int) -> bool:
        """Delete usuario by ID."""
        try:
            model = UsuarioModel.objects.get(usua_id=usua_id)
            model.delete()
            return True
        except ObjectDoesNotExist:
            return False
        except Exception as e:
            raise RepositoryError(f"Error deleting usuario: {str(e)}")
    
    def list_all(self, active_only: bool = True) -> List[Usuario]:
        """List all usuarios."""
        queryset = UsuarioModel.objects.select_related('rous_id')
        
        if active_only:
            queryset = queryset.filter(usua_estado=1)
        
        return [self._model_to_entity(model) for model in queryset.all()]
    
    def list_by_role(self, rous_id: int, active_only: bool = True) -> List[Usuario]:
        """List usuarios by role."""
        queryset = UsuarioModel.objects.select_related('rous_id').filter(rous_id=rous_id)
        
        if active_only:
            queryset = queryset.filter(usua_estado=1)
        
        return [self._model_to_entity(model) for model in queryset.all()]
    
    def exists_email(self, usua_email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if email already exists."""
        queryset = UsuarioModel.objects.filter(usua_email=usua_email)
        
        if exclude_id:
            queryset = queryset.exclude(usua_id=exclude_id)
        
        return queryset.exists()
    
    def exists_rut(self, usua_rut: str, exclude_id: Optional[int] = None) -> bool:
        """Check if RUT already exists."""
        queryset = UsuarioModel.objects.filter(usua_rut=usua_rut)
        
        if exclude_id:
            queryset = queryset.exclude(usua_id=exclude_id)
        
        return queryset.exists()