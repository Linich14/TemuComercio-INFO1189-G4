"""
URL configuration for products API.
Maps URLs to our Clean Architecture views.
"""
from django.urls import path
from src.interfaces.api.views.product_views import (
    ProductListCreateView,
    ProductDetailView,
    ProductStockUpdateView
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/stock/', ProductStockUpdateView.as_view(), name='product-stock-update'),
]