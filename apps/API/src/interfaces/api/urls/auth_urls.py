"""
Auth URL patterns.
API routes for authentication endpoints.
"""
from django.urls import path
from ..views.auth_views import login_view, logout_view, verify_token_view

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', login_view, name='auth-login'),
    path('auth/logout/', logout_view, name='auth-logout'),
    path('auth/verify/', verify_token_view, name='auth-verify'),
]