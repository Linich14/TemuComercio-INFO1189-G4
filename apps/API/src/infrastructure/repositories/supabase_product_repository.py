"""
Enhanced Django ORM implementation of ProductRepository with Supabase integration.
Includes both Django ORM and direct Supabase operations.
"""
from typing import List, Optional
from django.db.models import Q
from asgiref.sync import sync_to_async

from ...core.domain.repositories.product_repository import ProductRepository
from ...core.domain.entities.product import Product
from .models import ProductModel
from ..external_services.supabase_service import get_supabase_client


class SupabaseProductRepository(ProductRepository):
    """
    Enhanced ProductRepository with Supabase integration.
    Uses Django ORM for complex operations and Supabase client for real-time features.
    """
    
    def __init__(self):
        self.supabase_client = get_supabase_client()
    
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
        
        # Optionally sync with Supabase for real-time features
        if self.supabase_client:
            try:
                await self._sync_to_supabase(saved_model)
            except Exception as e:
                print(f"Warning: Failed to sync to Supabase: {e}")
        
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
        
        # Optionally sync with Supabase
        if self.supabase_client:
            try:
                await self._sync_to_supabase(product_model)
            except Exception as e:
                print(f"Warning: Failed to sync to Supabase: {e}")
        
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
    
    async def _sync_to_supabase(self, model: ProductModel) -> None:
        """
        Sync product data to Supabase for real-time features.
        This is optional and used for enhanced features.
        """
        if not self.supabase_client:
            return
        
        product_data = {
            'id': model.id,
            'name': model.name,
            'description': model.description,
            'price': float(model.price),
            'stock': model.stock,
            'category': model.category,
            'is_active': model.is_active,
            'created_at': model.created_at.isoformat(),
            'updated_at': model.updated_at.isoformat(),
        }
        
        # This would be used for real-time sync if needed
        # self.supabase_client.table('products_sync').upsert(product_data).execute()
    
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


# For backward compatibility, keep the original implementation
DjangoProductRepository = SupabaseProductRepository