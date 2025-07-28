from django.http import JsonResponse
from django.shortcuts import render , redirect, get_object_or_404
from .models import Product, ProductCategory, Wishlist

def product_list(request):
    products = Product.objects.filter()
    categories = ProductCategory.objects.all()
    wishlist = get_wishlist(request)
    wishlist_products = wishlist.products.values_list('id', flat=True)

    context = {
        'products': products,
        'categories': categories,
        'wishlists': wishlist_products,
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


# def wishlist_view(request):
#     wishlist = get_wishlist(request)
#     items = wishlist.items.select_related('product')
#     return render(request, 'wishlist.html', {'items': items})


def get_wishlist(request):
    # Ensure session exists
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    wishlist, created = Wishlist.objects.get_or_create(session_key=session_key)
    return wishlist
def add_to_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        if not product_id:
            return JsonResponse({'success': False, 'error': 'No product ID provided.'})

        product = get_object_or_404(Product, id=product_id)
        wishlist = get_wishlist(request)

        if not wishlist.products.filter(id=product.id).exists():
            wishlist.products.add(product)

        wishlist.save()

        return JsonResponse({'success': True, 'message': 'Product added to wishlist.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


def remove_from_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        if not product_id:
            return JsonResponse({'success': False, 'error': 'No product ID provided.'})

        product = get_object_or_404(Product, id=product_id)
        wishlist = get_wishlist(request)

        if wishlist.products.filter(id=product.id).exists():
            wishlist.products.remove(product)

        wishlist.save()

        return JsonResponse({'success': True, 'message': 'Product removed from wishlist.'})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})