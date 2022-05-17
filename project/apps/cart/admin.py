from django.contrib import admin

from .models import Cart


class ProductsCartInlineAdmin(admin.StackedInline):
    model = Cart.products.through
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'created_at',)
    inlines = [ProductsCartInlineAdmin]
    ordering = 'created_at',
