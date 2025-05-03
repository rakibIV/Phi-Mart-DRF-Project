from rest_framework import serializers
from product.models import Product, Category, Review, ProductImage
from decimal import Decimal
from django.contrib.auth import get_user_model


    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']
        
    product_count = serializers.IntegerField(read_only=True, help_text="For counting total products under this category")


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id','image']
       

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name','images','description', 'stock', 'price', 'category', 'price_with_tax']
        
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self, product):
        return round(product.price * Decimal(1.2),2)
    
    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price must be greater than or equal to 0")
        return price
    
    

    
    

class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_current_user_name')
    class Meta:
        model = get_user_model()
        fields = ['id','name']
        
    def get_current_user_name(self,obj):
        return obj.get_full_name()
    
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields = ['id', 'user','product', 'comment','ratings']
        read_only_fields = ['user','product',]
        
    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        review = Review.objects.create(product_id=product_id, **validated_data)
        return review
    
