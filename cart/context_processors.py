from .models import CartItem, Cart

def cart_items_count(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart = Cart.objects.filter(session_key=session_key).first()
    if cart:
        count = CartItem.objects.filter(cart=cart).count()
    else:
        count = 0

    return {'cart_items_count': count}
