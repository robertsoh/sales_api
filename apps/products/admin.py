from django.contrib import admin
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail

from apps.products.models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):

    model = ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'parent')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'price', 'category', 'has_stock', 'active')
    search_fields = ('name',)
    list_filter = ('category', 'active', 'has_stock')
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = ('image', 'product', 'order')
    list_filter = ('product',)

    def image(self, obj):
        im = get_thumbnail(obj.file, '100x100', crop='center')
        return format_html('<img src="{}" />', im.url)
