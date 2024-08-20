from django.contrib import admin
from .models import Product, Profile, Colour, Image, Size, Cart, Supplier, Order, CartItem

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'title', 'category', 'price', 'stock', 'discount')
    search_fields = ('title', 'category', 'product_id')
    list_filter = ('category', 'price', 'stock')
    ordering = ('product_id',)

class ColourAdmin(admin.ModelAdmin):
    list_display = ('colour_id', 'product', 'colour')
    search_fields = ('colour', 'product__title')
    list_filter = ('colour',)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'product', 'image')
    search_fields = ('product__title',)
    list_filter = ('product__title',)

class SizeAdmin(admin.ModelAdmin):
    list_display = ('size_id', 'product', 'size')
    search_fields = ('size', 'product__title')
    list_filter = ('size',)

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_id', 'name', 'contact_number')
    search_fields = ('name', 'supplier_id')
    list_filter = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'delivery_status', 'order_date', 'total_amount', 'cart', 'supplier')
    search_fields = ('order_id', 'delivery_status', 'supplier__name')
    list_filter = ('delivery_status', 'order_date', 'total_amount')
    ordering = ('order_date',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'city')
    search_fields = ('user__username', 'address', 'city')
    list_filter = ('city',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user')
    search_fields = ('cart_id', 'user__username')
    list_filter = ('user',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Colour, ColourAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Profile, ProfileAdmin)
