"""
Product repository interface.
Follows Dependency Inversion Principle.
"""
from abc import abstractmethod
from typing import List, Optional
from .base_repository import BaseRepository
from ..entities.product import Product


class ProductRepository(BaseRepository[Product]):
    """
    Product repository interface.
    Infrastructure layer will implement this interface.
    """
    
    @abstractmethod
    async def get_by_category(self, category: str) -> List[Product]:
        """Get products by category."""
        pass
    
    @abstractmethod
    async def get_active_products(self) -> List[Product]:
        """Get only active products."""
        pass
    
    @abstractmethod
    async def search_by_name(self, name: str) -> List[Product]:
        """Search products by name."""
        pass
    
    @abstractmethod
    async def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock."""
        pass