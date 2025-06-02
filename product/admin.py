from django.contrib import admin
from product.models import Product, Category, ProductImage

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','stock')
# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)