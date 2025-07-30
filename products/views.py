from django.http import JsonResponse
from django.shortcuts import render , redirect, get_object_or_404
from .models import Product, ProductCategory, Wishlist
from django.views.decorators.http import require_POST


def product_list(request):
    products = Product.objects.filter()
    categories = ProductCategory.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:4]
    context = {
        'product': product,
        'related' : related_products
    }
    return render(request, 'products/product_detail.html', context)



def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def wishlist_page(request):
    session_key = get_session_key(request)
    try:
        wishlist = Wishlist.objects.get(session_key=session_key)
        products = wishlist.products.all()
    except Wishlist.DoesNotExist:
        products = []

    return render(request, 'products/wishlist_page.html', {
        'products': products
    })



def get_wishlist_items(request):
    session_key = get_session_key(request)
    try:
        wishlist = Wishlist.objects.get(session_key=session_key)
        product_ids = list(wishlist.products.values_list('id', flat=True))
    except Wishlist.DoesNotExist:
        product_ids = []

    return JsonResponse({'wishlist': product_ids})


@require_POST
def toggle_wishlist(request):
    session_key = get_session_key(request)
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    wishlist, created = Wishlist.objects.get_or_create(session_key=session_key)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        added = False
    else:
        wishlist.products.add(product)
        added = True

    return JsonResponse({'added': added})
