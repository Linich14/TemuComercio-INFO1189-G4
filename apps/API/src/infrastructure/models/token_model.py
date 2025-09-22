from django.db import models
from django.utils import timezone
from .user_model import CustomUser
import uuid


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='refresh_tokens')
    token = models.TextField(unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'auth_service'
        db_table = 'auth_refresh_tokens'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['user', 'revoked']),
            models.Index(fields=['expires_at']),
        ]
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        return not self.revoked and not self.is_expired()