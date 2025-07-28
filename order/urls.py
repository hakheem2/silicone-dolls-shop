from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    #path('stripe-payment/', views.stripe_payment, name='stripe_payment'),
    #path('paypal-payment/', views.paypal_payment, name='paypal_payment'),
]
