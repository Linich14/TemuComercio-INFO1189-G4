from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from ...domain.repositories.user_repository import UserRepositoryInterface
from ...domain.entities.user import User
from ...models import UserModel, RolUsuarioModel

class DjangoUserRepository(UserRepositoryInterface):
    """Implementación Django del repositorio de usuarios"""
    
    def create(self, user: User) -> User:
        """Crea un nuevo usuario"""
        # Obtener rol si se especifica
        role = None
        if user.id_role:
            try:
                role = RolUsuarioModel.objects.get(rous_id=user.id_role)
            except ObjectDoesNotExist:
                role = None
        
        # Crear usuario en Django
        django_user = UserModel.objects.create(
            usua_email=user.email,
            usua_pass=user.password,  # Ya viene hasheada
            usua_rut=user.rut,
            usua_estado=user.estado,
            rous_id=role
        )
        
        return self._model_to_entity(django_user)
    
    def update(self, user: User) -> User:
        """Actualiza un usuario existente"""
        try:
            django_user = UserModel.objects.get(usua_id=user.id)
            
            django_user.usua_email = user.email
            django_user.usua_rut = user.rut
            django_user.usua_estado = user.estado
            
            if user.id_role:
                try:
                    role = RolUsuarioModel.objects.get(rous_id=user.id_role)
                    django_user.rous_id = role
                except ObjectDoesNotExist:
                    pass
            
            if user.password:  # Solo actualizar si se proporciona nueva contraseña
                django_user.usua_pass = user.password
            
            django_user.save()
            return self._model_to_entity(django_user)
            
        except ObjectDoesNotExist:
            raise ValueError(f"Usuario con ID {user.id} no encontrado")
    
    def delete(self, user_id: str) -> bool:
        """Elimina un usuario (soft delete - marca como inactivo)"""
        try:
            django_user = UserModel.objects.get(usua_id=user_id)
            django_user.usua_estado = False
            django_user.save()
            return True
        except ObjectDoesNotExist:
            return False
    
    def exists_by_email(self, email: str) -> bool:
        """Verifica si existe un usuario con el email dado"""
        return UserModel.objects.filter(usua_email=email).exists()
    
    def exists_by_rut(self, rut: str) -> bool:
        """Verifica si existe un usuario con el RUT dado"""
        return UserModel.objects.filter(usua_rut=rut).exists()
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por ID"""
        try:
            django_user = UserModel.objects.get(usua_id=user_id)
            return self._model_to_entity(django_user)
        except ObjectDoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        try:
            django_user = UserModel.objects.get(usua_email=email)
            return self._model_to_entity(django_user)
        except ObjectDoesNotExist:
            return None
    
    def get_by_rut(self, rut: str) -> Optional[User]:
        """Obtiene un usuario por RUT"""
        try:
            django_user = UserModel.objects.get(usua_rut=rut)
            return self._model_to_entity(django_user)
        except ObjectDoesNotExist:
            return None
    
    def list_all(self, active_only: bool = True) -> List[User]:
        """Lista todos los usuarios"""
        queryset = UserModel.objects.all()
        if active_only:
            queryset = queryset.filter(usua_estado=True)
        
        return [self._model_to_entity(django_user) for django_user in queryset]
    
    def count_users(self, active_only: bool = True) -> int:
        """Cuenta el número de usuarios"""
        queryset = UserModel.objects.all()
        if active_only:
            queryset = queryset.filter(usua_estado=True)
        return queryset.count()
    
    # Métodos de compatibilidad con la interfaz del repositorio
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por email (alias para get_by_email)"""
        return self.get_by_email(email)
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        """Busca un usuario por ID (alias para get_by_id)"""
        return self.get_by_id(user_id)
    
    def save(self, user: User) -> User:
        """Guarda un usuario (create o update según tenga ID)"""
        if user.id:
            return self.update(user)
        else:
            return self.create(user)
    
    def _model_to_entity(self, user_model: UserModel) -> User:
        """Convierte un modelo Django a entidad de dominio"""
        return User(
            id=str(user_model.usua_id),
            email=user_model.usua_email,
            password=user_model.usua_pass,
            estado=user_model.usua_estado,
            rut=user_model.usua_rut,
            id_role=user_model.rous_id.rous_id if user_model.rous_id else None,
            created_at=user_model.usua_creado,
            updated_at=user_model.usua_actualizado
        )
    
    def _entity_to_model(self, user: User, user_model: UserModel = None) -> UserModel:
        """Convierte una entidad de dominio a modelo Django"""
        if user_model is None:
            user_model = UserModel()
        
        user_model.usua_email = user.email
        user_model.usua_pass = user.password
        user_model.usua_estado = user.estado
        user_model.usua_rut = user.rut
        
        if user.id_role:
            try:
                user_model.rous_id = RolUsuarioModel.objects.get(rous_id=user.id_role)
            except RolUsuarioModel.DoesNotExist:
                user_model.rous_id = None
        else:
            user_model.rous_id = None
            
        return user_model
    
    # Método obsoleto removido - mantenía inconsistencia
    def _to_domain_entity(self, django_user: UserModel) -> User:
        """Método obsoleto - usar _model_to_entity"""
        return self._model_to_entity(django_user)
