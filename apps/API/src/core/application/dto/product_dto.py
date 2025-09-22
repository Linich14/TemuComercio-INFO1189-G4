"""
Product DTOs for data transport between layers.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from .base_dto import BaseDTO, BaseRequestDTO, BaseResponseDTO


@dataclass
class ProductDTO(BaseDTO):
    """Product data transfer object."""
    id: Optional[int]
    name: str
    description: str
    price: Decimal
    stock: int
    category: str
    is_active: bool
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class CreateProductRequestDTO(BaseRequestDTO):
    """Request DTO for creating a product."""
    name: str
    description: str
    price: Decimal
    stock: int
    category: str


@dataclass
class UpdateProductRequestDTO(BaseRequestDTO):
    """Request DTO for updating a product."""
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    category: Optional[str] = None


@dataclass
class ProductResponseDTO(BaseResponseDTO):
    """Response DTO for product operations."""
    product: Optional[ProductDTO] = None


@dataclass
class ProductListResponseDTO(BaseResponseDTO):
    """Response DTO for product list operations."""
    products: list[ProductDTO] = None
    total_count: int = 0


@dataclass
class UpdateStockRequestDTO(BaseRequestDTO):
    """Request DTO for stock updates."""
    product_id: int
    quantity: int
    operation: str  # 'increase' or 'decrease'