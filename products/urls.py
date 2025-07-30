from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),   # e.g. /products/
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # e.g. /products/doll-slug/
    path('wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/load', views.get_wishlist_items, name='get_wishlist_items'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
]
