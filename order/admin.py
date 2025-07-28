from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    list_display = ('full_name', 'email', 'total_price_display','phone', 'address', 'city', 'country', 'created_at', 'paid')
    search_fields = ('full_name', 'email', 'address', 'city', 'country')
    list_filter = ('created_at', 'paid', 'city', 'country')
    ordering = ('-created_at',)

    def total_price_display(self, obj):
        return f"${obj.total_price():.2f}"
    total_price_display.short_description = "Total Price"

admin.site.register(Order, OrderAdmin)