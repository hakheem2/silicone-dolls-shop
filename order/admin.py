from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ('id', 'name', 'email', 'formatted_order_number', 'total_price_display', 'payment_method', 'phone', 'address', 'city', 'country', 'created_at', 'paid')
    search_fields = ('name', 'email', 'address', 'city', 'country', 'formatted_order_number')
    list_filter = ('created_at', 'paid', 'city', 'country',)
    ordering = ('-created_at',)

    def formatted_order_number(self, obj):
        return f"ORD-{obj.order_number}"

    formatted_order_number.short_description = "Order Number"

    def total_price_display(self, obj):
        return f"${obj.total_price():.2f}"
    total_price_display.short_description = "Total Price"

admin.site.register(Order, OrderAdmin)