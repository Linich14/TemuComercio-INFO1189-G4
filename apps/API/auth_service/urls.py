# interfaces/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .interfaces.views.auth_views import AuthViewSet

# Crear router para ViewSet
router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('api/', include(router.urls)),
]