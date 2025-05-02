from rest_framework import serializers
from order.models import Cart, CartItem, Order, OrderItem
from product.models import Product
from order.services import OrderServices



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']
        
        
class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
        
    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        print(cart_id)
        product = validated_data['product']
        quantity = validated_data['quantity']
        cart = Cart.objects.get(id=cart_id)
        cart_item = CartItem.objects.filter(cart= cart, product = product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(cart = cart, product=product, quantity = quantity)
        
            
        return cart_item
    
class CartItemUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only = True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        
    def get_total_price(self, cart_item : CartItem):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True, read_only = True)
    total_price = serializers.SerializerMethodField(method_name = 'get_total_price')
    class Meta :
        model = Cart
        fields = ['id', 'user','items','total_price']
        read_only_fields = ['user']
        
    def get_total_price(self, cart : Cart):
        return sum([item.product.price*item.quantity for item in cart.items.all()])
    
    
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk= cart_id).exists():
            raise serializers.ValidationError("No cart found with this id!")
        
        cart = Cart.objects.get(pk=cart_id)
        if not CartItem.objects.filter(cart= cart).exists():
            raise serializers.ValidationError("Cart is empty!")
        
        return cart_id
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']
        
        try:
            order = OrderServices.create_order(user_id=user_id,cart_id=cart_id)
            return order
        
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
        
    
    def to_representation(self, instance):
        return OrderSerializer(instance).data
    

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        
        
    def update(self, instance, validated_data):
        user = self.context['user']
        new_status = validated_data['status']
        
        if new_status == Order.CANCELED:
            return OrderServices.cancel_order(user,instance)
        
        if not user.is_staff:
            raise serializers.ValidationError({'detail':"You are not allowed to update the order!"})
        
        return super().update(instance,validated_data)


    
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','price','quantity','total_price']
    
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','user','status','total_price','created_at','items']
        
        
class EmptySerializer(serializers.Serializer):
    pass
        