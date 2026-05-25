from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
import json

from accounts.forms import UserRegisterForm
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review, Wishlist, SearchHistory


def home(request):
    featured = Product.objects.filter(is_featured=True)[:8]
    ai_picks = Product.objects.filter(is_ai_recommended=True)[:4]
    categories = Category.objects.all()
    top_deals = Product.objects.filter(amazon_price__isnull=False).order_by('-our_price')[:6]
    return render(request, 'store/home.html', {
        'featured': featured,
        'ai_picks': ai_picks,
        'categories': categories,
        'top_deals': top_deals,
    })


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search_q = request.GET.get('q', '')
    sort = request.GET.get('sort', 'default')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if search_q:
        products = products.filter(Q(name__icontains=search_q) | Q(description__icontains=search_q) | Q(brand__icontains=search_q) | Q(tags__icontains=search_q))
        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=search_q)
    if min_price:
        products = products.filter(our_price__gte=min_price)
    if max_price:
        products = products.filter(our_price__lte=max_price)
    if sort == 'price_low':
        products = products.order_by('our_price')
    elif sort == 'price_high':
        products = products.order_by('-our_price')
    elif sort == 'rating':
        products = products.order_by('-rating')

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'search_q': search_q,
        'selected_category': category_slug,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.user_reviews.all().order_by('-created_at')
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'related': related,
        'in_wishlist': in_wishlist,
    })


def compare_prices(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/compare.html', {'product': product})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'count': cart.items.count()})
    messages.success(request, f"'{product.name}' added to cart!")
    return redirect('store:cart')


@login_required
def cart(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    items = cart_obj.items.select_related('product').all()
    total = sum(item.subtotal() for item in items)
    return render(request, 'store/cart.html', {'items': items, 'total': total})


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('store:cart')


@login_required
def checkout(request):
    cart_obj, _ = Cart.objects.get_or_create(user=request.user)
    items = cart_obj.items.select_related('product').all()
    total = sum(item.subtotal() for item in items)
    if request.method == 'POST':
        address = request.POST.get('address', '')
        order = Order.objects.create(user=request.user, total=total, address=address)
        for item in items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.our_price)
        cart_obj.items.all().delete()
        messages.success(request, f"Order #{order.id} placed successfully!")
        return redirect('store:order_confirmation', pk=order.id)
    return render(request, 'store/checkout.html', {'items': items, 'total': total})


@login_required
def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'items': items})


@login_required
def toggle_wishlist(request, pk):
    product = get_object_or_404(Product, pk=pk)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        added = False
    else:
        added = True
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'added': added})
    return redirect('store:product_detail', pk=pk)


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        messages.success(request, "Review submitted!")
    return redirect('store:product_detail', pk=pk)


@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'store/dashboard.html', {'orders': orders, 'wishlist_count': wishlist_count})


@login_required(login_url='store:seller_login')
def seller_dashboard(request):
    if not request.user.groups.filter(name='Sellers').exists():
        messages.error(request, "Access Denied. You must log in with a Seller account to view the dashboard.")
        logout(request)
        return redirect('store:seller_login')

    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        our_price = request.POST.get('our_price')
        amazon_price = request.POST.get('amazon_price')
        flipkart_price = request.POST.get('flipkart_price')
        amazon_url = request.POST.get('amazon_url', '')
        flipkart_url = request.POST.get('flipkart_url', '')
        image_url = request.POST.get('image_url', '')
        brand = request.POST.get('brand', '')
        stock = request.POST.get('stock', 50)
        eco_rating = request.POST.get('eco_rating', 80)
        tags = request.POST.get('tags', '')

        category = get_object_or_404(Category, id=category_id)
        
        if not image_url:
            image_url = "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600" # fallback generic

        Product.objects.create(
            name=name,
            description=description,
            category=category,
            our_price=our_price,
            amazon_price=amazon_price if amazon_price else None,
            flipkart_price=flipkart_price if flipkart_price else None,
            amazon_url=amazon_url,
            flipkart_url=flipkart_url,
            image_url=image_url,
            brand=brand,
            stock=stock,
            eco_rating=eco_rating,
            tags=tags
        )
        messages.success(request, f"Product '{name}' successfully uploaded to NexCart!")
        return redirect('store:seller_dashboard')

    products = Product.objects.all().order_by('-created_at')
    return render(request, 'store/seller.html', {'categories': categories, 'products': products})


def seller_login(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Sellers').exists():
            return redirect('store:seller_dashboard')
        else:
            logout(request)

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.groups.filter(name='Sellers').exists():
                login(request, user)
                messages.success(request, f"Welcome back to Seller Center, {user.first_name or user.username}!")
                return redirect('store:seller_dashboard')
            else:
                messages.error(request, "This account is not registered as a Seller. Please register a seller account below.")
                return redirect('store:seller_login')
    else:
        form = AuthenticationForm()
    return render(request, 'store/seller_login.html', {'form': form})


def seller_register(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Sellers').exists():
            return redirect('store:seller_dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, _ = Group.objects.get_or_create(name='Sellers')
            user.groups.add(group)
            login(request, user)
            messages.success(request, f"Welcome to NexCart Seller Center, {user.first_name or user.username}! Start listing your inventory.")
            return redirect('store:seller_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'store/seller_register.html', {'form': form})
