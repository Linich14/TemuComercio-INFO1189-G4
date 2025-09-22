from django.db import models
from src.infrastructure.models.user_model import CustomUser
from src.infrastructure.models.token_model import RefreshToken

# Create your models here.
__all__ = ['CustomUser', 'RefreshToken']