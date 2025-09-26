# interfaces/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .interfaces.views.auth import (
    LoginAPIView,
    RegisterAPIView,
    RefreshTokenAPIView,
    ProfileAPIView,
    LogoutAPIView
)

# Crear router para ViewSet
router = DefaultRouter()

urlpatterns = [
    path('auth/login/', LoginAPIView.as_view(), name='auth-login'),
    path('auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('auth/refresh/', RefreshTokenAPIView.as_view(), name='auth-refresh'),
    path('auth/profile/', ProfileAPIView.as_view(), name='auth-profile'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth-logout'),
]