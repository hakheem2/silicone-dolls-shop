from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from cart.views import get_cart
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def checkout(request):
    # Get or create cart (adjust this as per your cart logic)
    cart = get_cart(request)

    # Fetch cart items with related product details
    cart_items_list = CartItem.objects.filter(cart=cart).select_related('product')

    cart_items = []
    total = 0

    for item in cart_items_list:
        subtotal = item.product.price * item.quantity
        total += subtotal
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })

    return render(request, 'order/checkout.html', {
        'cart_items': cart_items,
        'cart_total': total,
    })




@csrf_exempt
def process_checkout_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')

        cart = get_cart(request)
        cart_items_list = CartItem.objects.filter(cart=cart).select_related('product')

        if not cart_items_list:
            return JsonResponse({'error': 'Cart is empty'}, status=400)

        # Create the order record
        order = Order.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            country=country,
            payment_method=payment_method,
            paid=False,
        )

        total = 0
        cart_items = []

        # For each cart item, create an OrderItem
        for item in cart_items_list:
            subtotal = item.product.price * item.quantity
            total += subtotal
            cart_items.append({
                'product': item.product,
                'quantity': item.quantity,
                'subtotal': subtotal,
            })
            # Create OrderItem linked to this order
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Store order id in session for later use if needed
        request.session['order_id'] = order.id

        # Clear the cart
        cart_items_list.delete()

        # Send email after successful order creation
        send_order_email(order, cart_items)

        return JsonResponse({'message': 'Order placed and email sent successfully'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def send_order_email(order, cart_items):
    subject = f"New Order ORD-{order.order_number}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = ['support@carolineheusssiliconedolls.com', 'anyengmondesonmbaubeh@gmail.com']


    #or add order.email if sending to customer
    try:
        validate_email(order.email)
        to_email.append(order.email)
    except ValidationError:
        pass  # skip invalid email

    html_content = render_to_string('order/order_email.html', {
        'order': order,
        'cart_items': cart_items
    })

    msg = EmailMultiAlternatives(subject, '', from_email, to_email)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
    except Exception as e:
        # Log or silently fail
        print(f"Email failed: {e}")


def order_success(request):
    return render(request, 'order/order-success.html')