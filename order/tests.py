from django.test import TestCase

# Create your tests here.
def checkout(request):
    cart = get_cart(request)
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

    if request.method == 'POST':
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')

        if not all([full_name, email, phone, address, city, country, payment_method]):
            error_msg = 'Please fill in all fields, including payment method.'
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': error_msg}, status=400)
            messages.error(request, error_msg)
            return render(request, 'order/checkout.html', {
                'cart_items': cart_items,
                'cart_total': total,
            })

        # Create the Order
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            country=country,
            paid=False,
        )

        for item in cart_items_list:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Clear the cart
        cart_items_list.delete()

        # Store info in session
        request.session['payment_method'] = payment_method
        request.session['order_id'] = order.id

    return render(request, 'order/checkout.html', {
        'cart_items': cart_items,
        'cart_total': total,
    })