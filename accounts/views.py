from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm


def gateway(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Sellers').exists():
            return redirect('ai_features:ai_dashboard')
        else:
            return redirect('store:home')

    if request.method == 'POST':
        role = request.POST.get('role', 'customer')
        action = request.POST.get('action', 'signin')
        if action == 'signup':
            return redirect(f'/accounts/register/?role={role}')
        else:
            return redirect(f'/accounts/login/?role={role}')

    return render(request, 'accounts/gateway.html')


def register(request):
    role = request.GET.get('role', 'customer')
    if request.method == 'POST':
        role = request.POST.get('role', role)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if role == 'seller':
                from django.contrib.auth.models import Group
                group, _ = Group.objects.get_or_create(name='Sellers')
                user.groups.add(group)
            login(request, user)
            if role == 'seller':
                messages.success(request, f"Welcome to NexCart Seller Center, {user.first_name or user.username}! Start listing your inventory.")
                return redirect('ai_features:ai_dashboard')
            else:
                messages.success(request, f"Welcome to NexCart AI, {user.first_name or user.username}!")
                return redirect('store:home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form, 'role': role})


def login_view(request):
    role = request.GET.get('role', 'customer')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.groups.filter(name='Sellers').exists():
                messages.success(request, f"Welcome back to Seller Center, {user.first_name or user.username}!")
                return redirect('ai_features:ai_dashboard')
            else:
                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect(request.GET.get('next', 'store:home'))
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'role': role})


def logout_view(request):
    logout(request)
    return redirect('accounts:gateway')
