"""
Product use cases - Application layer.
Contains business logic orchestration.
"""
from typing import List
from ..dto.product_dto import (
    CreateProductRequestDTO,
    ProductResponseDTO,
    ProductListResponseDTO,
    UpdateStockRequestDTO,
    ProductDTO
)
from ..dto.base_dto import BaseResponseDTO
from .base_use_case import BaseUseCase
from ...domain.entities.product import Product
from ...domain.repositories.product_repository import ProductRepository


class CreateProductUseCase(BaseUseCase[CreateProductRequestDTO, ProductResponseDTO]):
    """
    Use case for creating a new product.
    Follows Single Responsibility Principle.
    """
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    async def execute(self, request: CreateProductRequestDTO) -> ProductResponseDTO:
        """Create a new product."""
        try:
            # Create domain entity
            product = Product(
                name=request.name,
                description=request.description,
                price=request.price,
                stock=request.stock,
                category=request.category
            )
            
            # Save through repository
            saved_product = await self._product_repository.create(product)
            
            # Convert to DTO
            product_dto = self._to_dto(saved_product)
            
            return ProductResponseDTO(
                success=True,
                message="Product created successfully",
                product=product_dto
            )
            
        except Exception as e:
            return ProductResponseDTO(
                success=False,
                message=f"Error creating product: {str(e)}"
            )


class GetProductByIdUseCase(BaseUseCase[int, ProductResponseDTO]):
    """Use case for getting a product by ID."""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    async def execute(self, product_id: int) -> ProductResponseDTO:
        """Get product by ID."""
        try:
            product = await self._product_repository.get_by_id(product_id)
            
            if not product:
                return ProductResponseDTO(
                    success=False,
                    message="Product not found"
                )
            
            product_dto = self._to_dto(product)
            
            return ProductResponseDTO(
                success=True,
                message="Product retrieved successfully",
                product=product_dto
            )
            
        except Exception as e:
            return ProductResponseDTO(
                success=False,
                message=f"Error retrieving product: {str(e)}"
            )


class GetAllProductsUseCase(BaseUseCase[None, ProductListResponseDTO]):
    """Use case for getting all products."""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    async def execute(self, request: None = None) -> ProductListResponseDTO:
        """Get all products."""
        try:
            products = await self._product_repository.get_all()
            
            product_dtos = [self._to_dto(product) for product in products]
            
            return ProductListResponseDTO(
                success=True,
                message="Products retrieved successfully",
                products=product_dtos,
                total_count=len(product_dtos)
            )
            
        except Exception as e:
            return ProductListResponseDTO(
                success=False,
                message=f"Error retrieving products: {str(e)}",
                products=[],
                total_count=0
            )


class UpdateStockUseCase(BaseUseCase[UpdateStockRequestDTO, BaseResponseDTO]):
    """Use case for updating product stock."""
    
    def __init__(self, product_repository: ProductRepository):
        self._product_repository = product_repository
    
    async def execute(self, request: UpdateStockRequestDTO) -> BaseResponseDTO:
        """Update product stock."""
        try:
            product = await self._product_repository.get_by_id(request.product_id)
            
            if not product:
                return BaseResponseDTO(
                    success=False,
                    message="Product not found"
                )
            
            # Apply business logic
            if request.operation == "increase":
                product.increase_stock(request.quantity)
            elif request.operation == "decrease":
                product.reduce_stock(request.quantity)
            else:
                return BaseResponseDTO(
                    success=False,
                    message="Invalid operation. Use 'increase' or 'decrease'"
                )
            
            # Save changes
            await self._product_repository.update(product)
            
            return BaseResponseDTO(
                success=True,
                message=f"Stock {request.operation}d successfully"
            )
            
        except Exception as e:
            return BaseResponseDTO(
                success=False,
                message=f"Error updating stock: {str(e)}"
            )


def _to_dto(product: Product) -> ProductDTO:
    """Convert domain entity to DTO."""
    return ProductDTO(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        category=product.category,
        is_active=product.is_active,
        created_at=product.created_at.isoformat() if product.created_at else None,
        updated_at=product.updated_at.isoformat() if product.updated_at else None
    )