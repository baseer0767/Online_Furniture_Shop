from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from about.models import Product



# @login_required
def home(request):
    discounted_products = Product.objects.filter(discount__gt=0)
    low_stock_products = Product.objects.filter(stock__lt=10)
    context = {
        'products': discounted_products,
        'hot_products': low_stock_products
    }
    return render(request, 'home.html', context)


# @login_required
def checkout(request):
    return render(request,'checkout.html')