"""
Validation services for domain entities.
Domain layer - Pure business logic validation.
"""
import re
from typing import Protocol


class EmailValidator(Protocol):
    """Protocol for email validation."""
    
    def validate(self, email: str) -> bool:
        """Validate email format."""
        ...


class RutValidator(Protocol):
    """Protocol for RUT validation."""
    
    def validate(self, rut: str) -> bool:
        """Validate Chilean RUT format."""
        ...


class DomainEmailValidator:
    """Domain implementation of email validation."""
    
    def validate(self, email: str) -> bool:
        """
        Basic email validation following RFC standards.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email format is valid
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class DomainRutValidator:
    """Domain implementation of Chilean RUT validation."""
    
    def validate(self, rut: str) -> bool:
        """
        Basic RUT validation (Chilean ID format).
        
        Args:
            rut: RUT to validate
            
        Returns:
            True if RUT format is valid
        """
        # Remove formatting
        clean_rut = rut.replace("-", "").replace(".", "")
        
        # Must have at least 8 characters (7 digits + verification digit)
        if len(clean_rut) < 8:
            return False
            
        # Basic format validation
        return clean_rut[:-1].isdigit()