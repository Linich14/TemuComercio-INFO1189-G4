# interfaces/api/urls.py
from django.urls import path
from src.interfaces.api.views.auth_views import LoginAPIView, RegisterAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]