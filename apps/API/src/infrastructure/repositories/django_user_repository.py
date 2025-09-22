from django.contrib.auth import get_user_model
from django.utils import timezone
from ...core.domain.repositories.user_repository import UserRepositoryInterface
from ...core.domain.entities.user import User
from ..models.user_model import CustomUser
from typing import Optional

CustomUser = get_user_model()

class DjangoUserRepository(UserRepositoryInterface):
    
    def find_by_email(self, email: str) -> Optional[User]:
        try:
            django_user = CustomUser.objects.get(email=email)
            return self._to_domain_entity(django_user)
        except CustomUser.DoesNotExist:
            return None
    
    def create(self, user: User) -> User:
        django_user = CustomUser.objects.create_user(
            email=user.email,
            password=user.password_hash,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            rut=user.rut,
            avatar=user.avatar,
            birth_date=user.birth_date,
            is_active=user.is_active,
            is_verified=user.is_verified
        )
        return self._to_domain_entity(django_user)
    
    def exists_by_email(self, email: str) -> bool:
        return CustomUser.objects.filter(email=email).exists()
    
    def exists_by_rut(self, rut: str) -> bool:
        return CustomUser.objects.filter(rut=rut).exists()
    
    def update_last_login(self, user_id: int) -> None:
        CustomUser.objects.filter(id=user_id).update(
            last_login=timezone.now()
        )
    
    def _to_domain_entity(self, django_user: CustomUser) -> User:
        return User(
            id=django_user.id,
            email=django_user.email,
            password_hash=django_user.password,
            first_name=django_user.first_name,
            last_name=django_user.last_name,
            phone=django_user.phone,
            rut=django_user.rut,
            avatar=django_user.avatar,
            birth_date=django_user.birth_date,
            is_active=django_user.is_active,
            is_verified=django_user.is_verified,
            created_at=django_user.created_at,
            last_login=django_user.last_login
        )