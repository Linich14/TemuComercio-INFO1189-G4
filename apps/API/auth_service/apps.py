from django.apps import AppConfig

class AuthServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_service'
    verbose_name = 'Servicio de Autenticación'
    
    def ready(self):
        """Se ejecuta cuando la aplicación está lista"""
        # Importar señales u otras configuraciones si es necesario
        pass


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_service'
    label = 'auth_service' 
    verbose_name = 'Custom Authentication'

