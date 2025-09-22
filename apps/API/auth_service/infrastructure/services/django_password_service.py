import secrets
import string
import re
from django.contrib.auth.hashers import make_password, check_password
from ...domain.services.password_service import PasswordServiceInterface

class DjangoPasswordService(PasswordServiceInterface):
    """Implementación Django del servicio de contraseñas"""
    
    def hash_password(self, password: str) -> str:
        """Hashea una contraseña usando el hasher de Django"""
        return make_password(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""
        return check_password(plain_password, hashed_password)
    
    def generate_password(self, length: int = 12) -> str:
        """Genera una contraseña aleatoria"""
        if length < 8:
            length = 8
        
        # Asegurar que tenga al menos uno de cada tipo
        characters = (
            secrets.choice(string.ascii_lowercase) +
            secrets.choice(string.ascii_uppercase) +
            secrets.choice(string.digits) +
            secrets.choice("!@#$%^&*")
        )
        
        # Completar el resto
        all_characters = string.ascii_letters + string.digits + "!@#$%^&*"
        for _ in range(length - 4):
            characters += secrets.choice(all_characters)
        
        # Mezclar caracteres
        char_list = list(characters)
        secrets.SystemRandom().shuffle(char_list)
        return ''.join(char_list)
    
    def is_password_strong(self, password: str) -> bool:
        """Verifica si una contraseña es fuerte"""
        if len(password) < 8:
            return False
        
        # Verificar que tenga al menos una minúscula, mayúscula, número y símbolo
        checks = [
            re.search(r'[a-z]', password),  # minúscula
            re.search(r'[A-Z]', password),  # mayúscula
            re.search(r'[0-9]', password),  # número
            re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\?]', password),  # símbolo
        ]
        
        return all(checks)
