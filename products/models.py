from django.db import models
import random
from django.utils.text import slugify

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    sex = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    size = models.CharField(max_length=100, null=True, blank=True)
    weight = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    no_in_stock = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='products/main/')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    reviews = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # Auto-generate size if not set
        if not self.size:
            self.size = f"{random.randint(18, 23)} inch"

        #Auto-generate ratings
        if not self.rating:
            self.rating = round(random.uniform(4.1, 4.9), 1)

        #Auto-generate reviews
        if not self.reviews:
            self.reviews = random.randint(94, 305)

         #Auto-generate no_in_stock
        if not self.no_in_stock:
            self.no_in_stock = random.randint(7, 15)

        # Auto-generate weight if not set
        if not self.weight:
            self.weight = f"{random.randint(5, 10)} lbs"
        super().save(*args, **kwargs)

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"{self.product.name} - Gallery Image"


class Wishlist(models.Model):
    session_key = models.CharField(max_length=100, db_index=True)
    products = models.ManyToManyField(Product, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist {self.id} - Session {self.session_key}"


