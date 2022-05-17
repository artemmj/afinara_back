from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from .models import Order
from apps.cart.models import Cart


class ProductsCartInlineAdmin(NestedStackedInline):
    model = Cart.products.through
    extra = 0


class CartAdmin(NestedStackedInline):
    model = Cart
    extra = 1
    inlines = [ProductsCartInlineAdmin]


@admin.register(Order)
class OrderAdmin(NestedModelAdmin):
    fields = ('delivery_type', 'fio', 'email', 'phone', 'inn', 'comment', 'requisites')
    raw_id_fields = ('requisites',)
    list_display = (
        'id', 'created_at', 'delivery_type', 'fio', 'email', 'phone',
    )
    ordering = ('-created_at',)
    inlines = [CartAdmin]
