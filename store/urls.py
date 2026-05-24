from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('shop/', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/compare/', views.compare_prices, name='compare_prices'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:pk>/confirmation/', views.order_confirmation, name='order_confirmation'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:pk>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('review/add/<int:pk>/', views.add_review, name='add_review'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/login/', views.seller_login, name='seller_login'),
    path('seller/register/', views.seller_register, name='seller_register'),
]
