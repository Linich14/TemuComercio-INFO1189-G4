from typing import Optional, List
from django.core.exceptions import ObjectDoesNotExist
from ...models import UserModel, RolUsuarioModel
from ...domain.repositories.user_repository import UserRepositoryInterface
from ...domain.entities.user import User

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
            email=user.email,
            password=user.password,  # Ya viene hasheada
            first_name=user.first_name,
            last_name=user.last_name,
            rut=user.rut,
            rous_id=role,
            is_active=user.is_active
        )
        
        return self._to_domain_entity(django_user)
    
    def update(self, user: User) -> User:
        """Actualiza un usuario existente"""
        try:
            django_user = UserModel.objects.get(id=user.id)
            
            django_user.email = user.email
            django_user.first_name = user.first_name
            django_user.last_name = user.last_name
            django_user.rut = user.rut
            django_user.is_active = user.is_active
            
            if user.id_role:
                try:
                    role = RolUsuarioModel.objects.get(rous_id=user.id_role)
                    django_user.rous_id = role
                except ObjectDoesNotExist:
                    pass
            
            if user.password:  # Solo actualizar si se proporciona nueva contraseña
                django_user.password = user.password
            
            django_user.save()
            return self._to_domain_entity(django_user)
            
        except ObjectDoesNotExist:
            raise ValueError(f"Usuario con ID {user.id} no encontrado")
    
    def delete(self, user_id: str) -> bool:
        """Elimina un usuario (soft delete - marca como inactivo)"""
        try:
            django_user = UserModel.objects.get(id=user_id)
            django_user.is_active = False
            django_user.save()
            return True
        except ObjectDoesNotExist:
            return False
    
    def exists_by_email(self, email: str) -> bool:
        """Verifica si existe un usuario con el email dado"""
        return UserModel.objects.filter(email=email).exists()
    
    def exists_by_rut(self, rut: str) -> bool:
        """Verifica si existe un usuario con el RUT dado"""
        return UserModel.objects.filter(rut=rut).exists()
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por ID"""
        try:
            django_user = UserModel.objects.get(id=user_id)
            return self._to_domain_entity(django_user)
        except ObjectDoesNotExist:
            return None
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        try:
            django_user = UserModel.objects.get(email=email)
            return self._to_domain_entity(django_user)
        except ObjectDoesNotExist:
            return None
    
    def get_by_rut(self, rut: str) -> Optional[User]:
        """Obtiene un usuario por RUT"""
        try:
            django_user = UserModel.objects.get(rut=rut)
            return self._to_domain_entity(django_user)
        except ObjectDoesNotExist:
            return None
    
    def list_all(self, active_only: bool = True) -> List[User]:
        """Lista todos los usuarios"""
        queryset = UserModel.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True)
        
        return [self._to_domain_entity(django_user) for django_user in queryset]
    
    def count_users(self, active_only: bool = True) -> int:
        """Cuenta el número de usuarios"""
        queryset = UserModel.objects.all()
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.count()
    
    def _to_domain_entity(self, django_user: UserModel) -> User:
        """Convierte un modelo Django a entidad del dominio"""
        return User(
            id=str(django_user.id),
            email=django_user.email,
            password=django_user.password,
            first_name=django_user.first_name,
            last_name=django_user.last_name,
            rut=django_user.rut,
            id_role=django_user.rous_id.rous_id if django_user.rous_id else None,
            is_active=django_user.is_active,
            created_at=django_user.created_at,
            updated_at=django_user.updated_at
        )
