"""
API serializers for product endpoints.
Interface layer - converts between API and application layer.
"""
from rest_framework import serializers
from decimal import Decimal


class ProductSerializer(serializers.Serializer):
    """
    Serializer for Product data.
    Follows Single Responsibility - only handles serialization.
    """
    
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField(min_value=0)
    category = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CreateProductSerializer(serializers.Serializer):
    """Serializer for creating products."""
    
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    stock = serializers.IntegerField(min_value=0)
    category = serializers.CharField(max_length=100)


class UpdateStockSerializer(serializers.Serializer):
    """Serializer for stock updates."""
    
    quantity = serializers.IntegerField(min_value=1)
    operation = serializers.ChoiceField(choices=['increase', 'decrease'])


class ProductResponseSerializer(serializers.Serializer):
    """Response serializer for product operations."""
    
    success = serializers.BooleanField()
    message = serializers.CharField()
    product = ProductSerializer(required=False, allow_null=True)


class ProductListResponseSerializer(serializers.Serializer):
    """Response serializer for product list operations."""
    
    success = serializers.BooleanField()
    message = serializers.CharField()
    products = ProductSerializer(many=True, required=False)
    total_count = serializers.IntegerField()