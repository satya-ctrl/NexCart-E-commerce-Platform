from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review, Wishlist

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Wishlist)

admin.site.site_header = "AI E-Commerce Admin"
admin.site.site_title = "AI E-Commerce"
