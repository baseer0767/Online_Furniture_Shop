# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from about.models import Cart, CartItem

@login_required
def cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
    
    cart_items = CartItem.objects.filter(cart=cart)

    cart_subtotal = sum(item.get_total_price() for item in cart_items)
    cart_total = cart_subtotal  # Add any additional charges if necessary

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'cart_subtotal': cart_subtotal,
        'cart_total': cart_total,
    }

    return render(request, 'cart.html', context)


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, cart_item_id=item_id, cart__user=request.user)
    
    # Update product stock
    cart_item.product.stock += cart_item.quantity
    cart_item.product.save()
    
    cart_item.delete()
    return redirect('cart')
