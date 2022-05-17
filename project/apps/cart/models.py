from django.db import models
from django.db.models import Sum, F, FloatField

from apps.helpers.models import UUIDModel, CreatedModel
from apps.catalog.models import Product
from apps.order.models import Order


class Cart(UUIDModel, CreatedModel):
    products = models.ManyToManyField(
        Product,
        verbose_name='Товары в корзине',
        related_name='carts',
        blank=True,
        through='CartProductRelationship',
    )
    order = models.OneToOneField(Order, models.CASCADE, related_name='order', null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return str(self.id)

    def total_amount(self):
        result = self.products.all().aggregate(
            total_amount=Sum(
                F('cart_product_relationship__count') * F('cart_product_relationship__product__price'),
                output_field=FloatField()
            )
        )
        return result['total_amount'] if 'total_amount' in result else 0


class CartProductRelationship(UUIDModel, CreatedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product_relationship')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    count = models.PositiveSmallIntegerField(verbose_name='Товаров в корзине', default=0)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.cart} - {self.product}'

    def total_cost(self):
        if self.product.price:
            return float(self.count) * float(self.product.price)
        else:
            return None
