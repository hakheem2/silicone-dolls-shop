from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'created_at', 'total_items_display')
    inlines = [CartItemInline]

    def total_items_display(self, obj):
        return obj.total_items()
    total_items_display.short_description = "Total Items"

admin.site.register(Cart, CartAdmin)
