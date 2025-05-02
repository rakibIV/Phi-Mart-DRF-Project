from order.models import Order, OrderItem, Cart, CartItem
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


class OrderServices:
    
    @staticmethod
    def create_order(user_id, cart_id):
        
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('product').all()
            total_price = sum([item.product.price*item.quantity for item in cart_items])
            
            order = Order.objects.create(user_id = user_id, total_price = total_price)
            
            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity,
                    total_price = item.product.price*item.quantity
                )
                for item in cart_items
            ]
            
            OrderItem.objects.bulk_create(order_items)
            
            cart.delete()
            
            return order
        
    def cancel_order(user,order):
        print("in cancel func.....")
        if user.is_staff:
            print('is staff......')
            order.status = Order.CANCELED
            order.save()
            return order
        
        if user != order.user:
            print('other user....')
            raise PermissionDenied({"detail" : "You can only cancel your own order!"})
        
        if order.status == Order.DELIVERED:
            print('delivered......')
            raise ValidationError({'detail':"Your product is already delivered. So, you can't cancel the order now!"})
        
        print('before assigning....')
        order.status = Order.CANCELED
        print('cancel assigned.....')
        order.save()
        print('saving...........')
        return order