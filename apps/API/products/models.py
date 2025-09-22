"""
Django models for products app.
Imports the actual model from infrastructure layer.
"""
from django.db import models

# Import from infrastructure layer to maintain clean architecture
from src.infrastructure.repositories.models import ProductModel

# Re-export for Django admin and migrations
__all__ = ['ProductModel']
