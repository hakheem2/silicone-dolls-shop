from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),   # e.g. /products/
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # e.g. /products/doll-slug/
    #path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove', views.remove_from_wishlist, name='remove_from_wishlist'),
]
