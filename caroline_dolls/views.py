from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.order_by('?')[:8]  # random 8 products
    return render(request, 'index.html', {'featured_products': products})
