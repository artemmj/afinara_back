from django import forms
from django.shortcuts import get_object_or_404

from service_objects.services import Service

from apps.cart.models import CartProductRelationship, Cart


class AddItemToCartService(Service):
    product = forms.UUIDField()
    cart = forms.UUIDField()
    count = forms.IntegerField(required=False)

    def process(self):
        product_id = self.cleaned_data['product']
        cart_id = self.cleaned_data['cart']
        count = self.cleaned_data['count']

        item, _ = CartProductRelationship.objects.get_or_create(
            product_id=product_id,
            cart_id=cart_id
        )
        if count:
            item.count += count
        else:
            item.count += 1
        item.save()
        return item.cart


class SetItemToCartService(Service):
    product = forms.UUIDField()
    cart = forms.UUIDField()
    count = forms.IntegerField()

    def process(self):
        product_id = self.cleaned_data['product']
        cart_id = self.cleaned_data['cart']
        count = self.cleaned_data['count']

        item, _ = CartProductRelationship.objects.get_or_create(
            product_id=product_id,
            cart_id=cart_id
        )
        if count == 0:
            item.delete()
        else:
            item.count = count
            item.save()
        return item.cart


class DeleteItemFromCartServise(Service):
    product = forms.UUIDField()
    cart = forms.UUIDField()

    def process(self):
        product_id = self.cleaned_data['product']
        cart_id = self.cleaned_data['cart']

        item = get_object_or_404(
            CartProductRelationship,
            product_id=product_id,
            cart_id=cart_id
        )
        if item.count >= 1:
            item.count -= 1
            item.save()
            if item.count == 0:
                item.delete()
        return item.cart


class DeletePositionFromCartService(Service):
    product = forms.UUIDField()
    cart = forms.UUIDField()

    def process(self):
        product_id = self.cleaned_data['product']
        cart_id = self.cleaned_data['cart']

        item = get_object_or_404(
            CartProductRelationship,
            cart_id=cart_id,
            product_id=product_id
        )
        item.delete()
        return item.cart


class ClearCartService(Service):
    cart = forms.UUIDField()

    def process(self):
        cart_id = self.cleaned_data['cart']
        cart = get_object_or_404(Cart, pk=cart_id)
        cart.cart_products.all().delete()
        return cart
