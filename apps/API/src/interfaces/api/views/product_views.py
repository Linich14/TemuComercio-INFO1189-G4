"""
API views for product endpoints.
Interface layer - handles HTTP requests and responses.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from ..serializers.product_serializers import (
    CreateProductSerializer,
    UpdateStockSerializer,
    ProductResponseSerializer,
    ProductListResponseSerializer
)
from ....core.application.use_cases.product_use_cases import (
    CreateProductUseCase,
    GetProductByIdUseCase,
    GetAllProductsUseCase,
    UpdateStockUseCase
)
from ....core.application.dto.product_dto import (
    CreateProductRequestDTO,
    UpdateStockRequestDTO
)


class ProductListCreateView(APIView):
    """
    API view for listing and creating products.
    Follows Single Responsibility - handles HTTP concerns only.
    """
    
    permission_classes = [AllowAny]  # For demo purposes
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Dependency injection will be configured later
        from ....infrastructure.repositories.supabase_product_repository import SupabaseProductRepository
        
        self._product_repository = SupabaseProductRepository()
        self._create_product_use_case = CreateProductUseCase(self._product_repository)
        self._get_all_products_use_case = GetAllProductsUseCase(self._product_repository)
    
    async def get(self, request):
        """Get all products."""
        try:
            result = await self._get_all_products_use_case.execute()
            
            serializer = ProductListResponseSerializer(result)
            
            if result.success:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Unexpected error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    async def post(self, request):
        """Create a new product."""
        try:
            serializer = CreateProductSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {'success': False, 'message': 'Invalid data', 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convert to DTO
            create_request = CreateProductRequestDTO(**serializer.validated_data)
            
            # Execute use case
            result = await self._create_product_use_case.execute(create_request)
            
            response_serializer = ProductResponseSerializer(result)
            
            if result.success:
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(response_serializer.data, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Unexpected error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductDetailView(APIView):
    """API view for individual product operations."""
    
    permission_classes = [AllowAny]  # For demo purposes
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Dependency injection will be configured later
        from ....infrastructure.repositories.supabase_product_repository import SupabaseProductRepository
        
        self._product_repository = SupabaseProductRepository()
        self._get_product_use_case = GetProductByIdUseCase(self._product_repository)
    
    async def get(self, request, product_id):
        """Get product by ID."""
        try:
            result = await self._get_product_use_case.execute(product_id)
            
            serializer = ProductResponseSerializer(result)
            
            if result.success:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Unexpected error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProductStockUpdateView(APIView):
    """API view for updating product stock."""
    
    permission_classes = [AllowAny]  # For demo purposes
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Dependency injection will be configured later
        from ....infrastructure.repositories.supabase_product_repository import SupabaseProductRepository
        
        self._product_repository = SupabaseProductRepository()
        self._update_stock_use_case = UpdateStockUseCase(self._product_repository)
    
    async def patch(self, request, product_id):
        """Update product stock."""
        try:
            serializer = UpdateStockSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {'success': False, 'message': 'Invalid data', 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Convert to DTO
            update_request = UpdateStockRequestDTO(
                product_id=product_id,
                **serializer.validated_data
            )
            
            # Execute use case
            result = await self._update_stock_use_case.execute(update_request)
            
            if result.success:
                return Response({'success': True, 'message': result.message}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False, 'message': result.message}, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response(
                {'success': False, 'message': f'Unexpected error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )