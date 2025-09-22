"""
Product entity - Domain layer example.
Represents a product in the e-commerce domain.
"""
from typing import Optional
from decimal import Decimal
from dataclasses import dataclass
from .base_entity import BaseEntity


@dataclass
class Product(BaseEntity):
    """
    Product entity following Domain-Driven Design.
    Contains business logic and validation rules.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        price: Decimal,
        stock: int,
        category: str,
        id: Optional[int] = None
    ):
        super().__init__(id)
        self._name = name
        self._description = description
        self._price = price
        self._stock = stock
        self._category = category
        self._is_active = True
        
        # Validate on creation
        self._validate()
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def price(self) -> Decimal:
        return self._price
    
    @property
    def stock(self) -> int:
        return self._stock
    
    @property
    def category(self) -> str:
        return self._category
    
    @property
    def is_active(self) -> bool:
        return self._is_active
    
    def update_price(self, new_price: Decimal) -> None:
        """Update product price with business validation."""
        if new_price <= 0:
            raise ValueError("Price must be greater than zero")
        
        self._price = new_price
        self.update_timestamp()
    
    def reduce_stock(self, quantity: int) -> None:
        """Reduce stock with business validation."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        if self._stock < quantity:
            raise ValueError("Insufficient stock")
        
        self._stock -= quantity
        self.update_timestamp()
    
    def increase_stock(self, quantity: int) -> None:
        """Increase stock."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        
        self._stock += quantity
        self.update_timestamp()
    
    def deactivate(self) -> None:
        """Deactivate product."""
        self._is_active = False
        self.update_timestamp()
    
    def activate(self) -> None:
        """Activate product."""
        self._is_active = True
        self.update_timestamp()
    
    def is_available(self) -> bool:
        """Check if product is available for purchase."""
        return self._is_active and self._stock > 0
    
    def _validate(self) -> None:
        """Validate business rules."""
        if not self._name or len(self._name.strip()) == 0:
            raise ValueError("Product name is required")
        
        if self._price <= 0:
            raise ValueError("Price must be greater than zero")
        
        if self._stock < 0:
            raise ValueError("Stock cannot be negative")
        
        if not self._category or len(self._category.strip()) == 0:
            raise ValueError("Category is required")