from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from products.models import Product
from .models import Cart, CartItem
from django.views.decorators.http import require_POST

# Helper inside views.py (not utils.py)
def get_cart(request):
    # Get the current session key or create a new one if it doesn't exist
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    # Try to get the existing cart for this session
    cart = Cart.objects.filter(session_key=session_key).first()

    # If no cart exists, create a new one linked to the session key
    if not cart:
        cart = Cart.objects.create(session_key=session_key)

    return cart



# Add to cart view (AJAX endpoint)
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        cart = get_cart(request)

        # Add or update CartItem
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

        return JsonResponse({'success': True, 'cart_count': cart.items.count()})

    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


# update cart quantity
@require_POST
def update_cart(request):
    cart = get_cart(request)
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')

    try:
        product = Product.objects.get(id=product_id)
        quantity = int(quantity)
        cart_item = CartItem.objects.get(cart=cart, product=product)

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        return JsonResponse({'status': 'success'})

    except (Product.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)


# remove product from cart
def remove_from_cart(request):
    cart = get_cart(request)
    product_id = request.POST.get('product_id')

    try:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return JsonResponse({'status': 'success'})

    except (Product.DoesNotExist, CartItem.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)


# Cart detail page
def cart_detail(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart).select_related('product')
    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })
