from django.db import models
from django.utils import timezone
from products.models import Product
import random

class Order(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    order_number = models.CharField(max_length=6, unique=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.name}"

    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    total_price.short_description = "Total Price"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_unique_order_number()
        super().save(*args, **kwargs)

    def _generate_unique_order_number(self):
        while True:
            number = f"{random.randint(0, 999999):06d}"  # 6-digit zero-padded
            if not Order.objects.filter(order_number=number).exists():
                return number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity
