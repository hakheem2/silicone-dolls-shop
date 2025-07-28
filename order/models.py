from django.db import models
from django.utils import timezone
from products.models import Product

class Order(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.full_name}"


    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    total_price.short_description = "Total Price"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity
