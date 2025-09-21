"""
Usuario URL patterns.
API routes for Usuario endpoints.
"""
from django.urls import path
from ..views.usuario_views import (
    create_usuario,
    get_usuario,
    list_usuarios,
    update_usuario,
    disable_usuario,
    enable_usuario
)

urlpatterns = [
    # Usuario CRUD endpoints
    path('usuarios/', list_usuarios, name='usuario-list'),
    path('usuarios/create/', create_usuario, name='usuario-create'),
    path('usuarios/<int:usua_id>/', get_usuario, name='usuario-detail'),
    path('usuarios/<int:usua_id>/update/', update_usuario, name='usuario-update'),
    
    # Usuario status management
    path('usuarios/<int:usua_id>/disable/', disable_usuario, name='usuario-disable'),
    path('usuarios/<int:usua_id>/enable/', enable_usuario, name='usuario-enable'),
]