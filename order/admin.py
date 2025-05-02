from django.contrib import admin
from order.models import Order, OrderItem,Cart, CartItem
# Register your models here.

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    
admin.site.register(CartItem)


@admin.register(Order)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')
admin.site.register(OrderItem)

