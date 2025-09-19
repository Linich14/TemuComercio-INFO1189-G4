"""
Django ORM implementation of ProductRepository.
Infrastructure layer - adapts Django ORM to domain interface.
"""
from typing import List, Optional
from django.db.models import Q
from asgiref.sync import sync_to_async

from ...core.domain.repositories.product_repository import ProductRepository
from ...core.domain.entities.product import Product
from .models import ProductModel


class DjangoProductRepository(ProductRepository):
    """
    Django ORM implementation of ProductRepository.
    Follows Dependency Inversion Principle - implements domain interface.
    """
    
    async def create(self, entity: Product) -> Product:
        """Create a new product in the database."""
        product_model = ProductModel(
            name=entity.name,
            description=entity.description,
            price=entity.price,
            stock=entity.stock,
            category=entity.category,
            is_active=entity.is_active
        )
        
        saved_model = await sync_to_async(product_model.save)()
        await sync_to_async(product_model.refresh_from_db)()
        
        return self._to_entity(product_model)
    
    async def get_by_id(self, entity_id: int) -> Optional[Product]:
        """Get product by ID."""
        try:
            product_model = await sync_to_async(ProductModel.objects.get)(id=entity_id)
            return self._to_entity(product_model)
        except ProductModel.DoesNotExist:
            return None
    
    async def get_all(self) -> List[Product]:
        """Get all products."""
        product_models = await sync_to_async(list)(ProductModel.objects.all())
        return [self._to_entity(model) for model in product_models]
    
    async def update(self, entity: Product) -> Product:
        """Update an existing product."""
        product_model = await sync_to_async(ProductModel.objects.get)(id=entity.id)
        
        product_model.name = entity.name
        product_model.description = entity.description
        product_model.price = entity.price
        product_model.stock = entity.stock
        product_model.category = entity.category
        product_model.is_active = entity.is_active
        
        await sync_to_async(product_model.save)()
        
        return self._to_entity(product_model)
    
    async def delete(self, entity_id: int) -> bool:
        """Delete a product."""
        try:
            product_model = await sync_to_async(ProductModel.objects.get)(id=entity_id)
            await sync_to_async(product_model.delete)()
            return True
        except ProductModel.DoesNotExist:
            return False
    
    async def exists(self, entity_id: int) -> bool:
        """Check if product exists."""
        return await sync_to_async(ProductModel.objects.filter(id=entity_id).exists)()
    
    async def get_by_category(self, category: str) -> List[Product]:
        """Get products by category."""
        product_models = await sync_to_async(list)(
            ProductModel.objects.filter(category=category)
        )
        return [self._to_entity(model) for model in product_models]
    
    async def get_active_products(self) -> List[Product]:
        """Get only active products."""
        product_models = await sync_to_async(list)(
            ProductModel.objects.filter(is_active=True)
        )
        return [self._to_entity(model) for model in product_models]
    
    async def search_by_name(self, name: str) -> List[Product]:
        """Search products by name."""
        product_models = await sync_to_async(list)(
            ProductModel.objects.filter(name__icontains=name)
        )
        return [self._to_entity(model) for model in product_models]
    
    async def get_low_stock_products(self, threshold: int = 10) -> List[Product]:
        """Get products with low stock."""
        product_models = await sync_to_async(list)(
            ProductModel.objects.filter(stock__lte=threshold)
        )
        return [self._to_entity(model) for model in product_models]
    
    def _to_entity(self, model: ProductModel) -> Product:
        """Convert Django model to domain entity."""
        entity = Product(
            name=model.name,
            description=model.description,
            price=model.price,
            stock=model.stock,
            category=model.category,
            id=model.id
        )
        
        # Set internal state
        entity._is_active = model.is_active
        entity._created_at = model.created_at
        entity._updated_at = model.updated_at
        
        return entity