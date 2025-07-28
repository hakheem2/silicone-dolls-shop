from django.contrib import admin
from .models import Product, ProductCategory, ProductGallery


class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductGalleryInline]
    list_display = ('name', 'category', 'price', 'available', 'no_in_stock', 'created_at', 'slug')
    list_filter = ('category', 'available', 'sex')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)

