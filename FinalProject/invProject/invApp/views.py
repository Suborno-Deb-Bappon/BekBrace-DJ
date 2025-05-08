from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


# Create your views here.

#home view
@login_required
def home_view(request):
    return render(request, 'invApp/home.html')

#create view
@login_required
def product_create_view(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('product_list')
    return render(request, 'invApp/product_form.html', {'form': form})

#read view
@login_required
def product_list_view(request):
    if request.user.profile.role != 'admin':
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()
    return render(request, 'invApp/product_list.html', {'products': products})

#update view
@login_required
def product_update_view(request, product_id):
    if request.user.profile.role == 'admin':
        product = get_object_or_404(Product, product_id=product_id)
    else:
        product = get_object_or_404(Product, product_id=product_id, user=request.user)
        
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'invApp/product_form.html', {'form': form, 'product': product})

#delete view
@login_required
def product_delete_view(request, product_id):
    if request.user.profile.role == 'admin':
        product = get_object_or_404(Product, product_id=product_id)
    else:
        product = get_object_or_404(Product, product_id=product_id, user=request.user)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'invApp/product_confirm_delete.html', {'product': product})

@login_required
def logout_view(request):
    return render(request, 'invApp/logout.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('product_list')
    
    if request.method == 'POST': 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'invApp/signup.html', {'form': form})
