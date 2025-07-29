from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.process_checkout_form, name='process_checkout_form'),
    path('submit-order/', views.send_order_email, name='send_order_email'),
    path('order-success/', views.order_success, name='order_success'),
]
