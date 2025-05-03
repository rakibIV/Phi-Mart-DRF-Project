from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category, Review, ProductImage
from rest_framework import status
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.pagination import DefaultPagination
from api.permissions import IsAdimOrReadOnly
from product.permissions import IsReviewAuthorOrReadOnly
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name']
    ordering_fields = ['price', 'stock', 'updated_at']
    permission_classes = [IsAdimOrReadOnly]
    
    
    @swagger_auto_schema(
    operation_summary="For deleting a products",
    operation_description="Only admin can delete products",
    responses={
        "201": ProductSerializer,
        "400" : "Bad request"
    }
    )
    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if product.stock > 0:
            return Response({"error": "Cannot delete a product with stock greater than 0."}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdimOrReadOnly]
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id = self.kwargs.get('product_pk'))
    
    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))


    
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count('products')).all()
    serializer_class = CategorySerializer
    
    
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return Review.objects.select_related('product', 'user').filter(product_id=self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}
    



