from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    def ready(self):
        """Configure dependencies when Django starts."""
        from src.infrastructure.di.container import configure_dependencies
        configure_dependencies()
