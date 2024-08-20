
from django.shortcuts import render, get_object_or_404, redirect
from about.models import Product, Cart, CartItem,Supplier,Order
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import AddToCartForm

def shop(request):
    category = request.GET.get('category', None)
    if category and category.upper() != 'ALL':
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop.html', {'page_obj': page_obj, 'category': category})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST, product_id=product_id)
        if form.is_valid():
            size = form.cleaned_data['size']
            colour = form.cleaned_data['colour']
            quantity = form.cleaned_data['quantity']
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, size=size, colour=colour,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            # Update product stock
            product.stock -= quantity
            product.save()
            
            return redirect('cart')  # Redirect to the cart page after adding item
    else:
        form = AddToCartForm(product_id=product_id)

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'product.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST, product_id=product_id)
        if form.is_valid():
            size = form.cleaned_data['size']
            colour = form.cleaned_data['colour']
            quantity = form.cleaned_data['quantity']
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, size=size, colour=colour,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return redirect('cart')  # Redirect to the cart page after adding item
    else:
        form = AddToCartForm(product_id=product_id)

    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'product.html', context)



from django.utils import timezone
from django.contrib import messages
from django.db import transaction

def get_available_supplier():
    suppliers = Supplier.objects.all()
    for supplier in suppliers:
        ongoing_orders_count = Order.objects.filter(supplier=supplier, delivery_status='Pending').count()
        if ongoing_orders_count < 4:
            return supplier
    return None  # Return None if no supplier is available (handle this case in your view)
from django.urls import reverse

@login_required
def order_view(request, cart_id):
    created_at = timezone.now().date()
    cart = get_object_or_404(Cart, pk=cart_id, user=request.user)
    cart_items = cart.cart_items.all()
    total_amount = sum(item.product.get_discounted_price() * item.quantity for item in cart_items)
    
    supplier = get_available_supplier()
    
    if not supplier:
        # Handle the case where no supplier is available
        return render(request, 'order.html', {
            'cart': cart,
            'cart_items': cart_items,
            'total_amount': total_amount,
            'error': 'No available suppliers at the moment. Please try again later.',
            'created_at': created_at,
            'check': False  # Ensure the success flag is False in this case
        })
    
    if request.method == 'POST':
        with transaction.atomic():
            order = Order.objects.create(
                delivery_status='Pending',
                order_date=timezone.now(),
                total_amount=total_amount,
                cart=cart,
                supplier=supplier
            )
            # Clear cart items
            cart_items.delete()
        
        return redirect('order_success')  # Redirect to the order success page

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'supplier': supplier,
        'created_at': created_at,
        'check': False  # Ensure the success flag is False in this case
    }
    return render(request, 'order.html', context)


def order_success(request):
    return render(request, 'order_success.html')


