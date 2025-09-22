import re
from typing import List, Dict, Any
from ...domain.services.validation_service import ValidationServiceInterface

class ValidationService(ValidationServiceInterface):
    """Implementación del servicio de validación"""
    
    def validate_email(self, email: str) -> bool:
        """Valida formato de email"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_rut(self, rut: str) -> bool:
        """Valida formato y dígito verificador de RUT chileno"""
        if not rut:
            return False
        
        # Limpiar RUT
        rut = rut.replace(".", "").replace("-", "").upper().strip()
        
        if len(rut) < 8 or len(rut) > 9:
            return False
        
        # Separar número y dígito verificador
        rut_number = rut[:-1]
        check_digit = rut[-1]
        
        # Verificar que el número sea numérico
        if not rut_number.isdigit():
            return False
        
        # Calcular dígito verificador
        def calculate_check_digit(rut_num: str) -> str:
            reversed_digits = map(int, reversed(rut_num))
            factors = [2, 3, 4, 5, 6, 7]
            s = sum(d * factors[i % 6] for i, d in enumerate(reversed_digits))
            remainder = 11 - (s % 11)
            
            if remainder == 11:
                return '0'
            elif remainder == 10:
                return 'K'
            else:
                return str(remainder)
        
        expected_check_digit = calculate_check_digit(rut_number)
        return check_digit == expected_check_digit
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """Valida una contraseña y retorna detalles de validación"""
        errors = []
        
        if not password:
            errors.append("La contraseña es requerida")
            return {'is_valid': False, 'errors': errors}
        
        if len(password) < 8:
            errors.append("La contraseña debe tener al menos 8 caracteres")
        
        if not re.search(r'[a-z]', password):
            errors.append("La contraseña debe tener al menos una letra minúscula")
        
        if not re.search(r'[A-Z]', password):
            errors.append("La contraseña debe tener al menos una letra mayúscula")
        
        if not re.search(r'[0-9]', password):
            errors.append("La contraseña debe tener al menos un número")
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\?]', password):
            errors.append("La contraseña debe tener al menos un símbolo especial")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'strength': 'strong' if len(errors) == 0 else 'weak'
        }
    
    def validate_user_data(self, user_data: Dict[str, Any]) -> List[str]:
        """Valida datos completos de usuario"""
        errors = []
        
        # Validar email
        email = user_data.get('email', '')
        if not self.validate_email(email):
            errors.append("Email inválido")
        
        # Validar nombres
        first_name = user_data.get('first_name', '').strip()
        if not first_name:
            errors.append("Nombre es requerido")
        elif len(first_name) < 2:
            errors.append("Nombre debe tener al menos 2 caracteres")
        
        last_name = user_data.get('last_name', '').strip()
        if not last_name:
            errors.append("Apellido es requerido")
        elif len(last_name) < 2:
            errors.append("Apellido debe tener al menos 2 caracteres")
        
        # Validar RUT si se proporciona
        rut = user_data.get('rut')
        if rut and not self.validate_rut(rut):
            errors.append("RUT inválido")
        
        # Validar contraseña si se proporciona
        password = user_data.get('password')
        if password:
            password_validation = self.validate_password(password)
            if not password_validation['is_valid']:
                errors.extend(password_validation['errors'])
        
        return errors
