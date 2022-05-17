from rest_framework import serializers

from apps.cart.models import Cart, CartProductRelationship
from .pdf_creator.creator import create_pdf_cart
from ..catalog.serializers import ProductSerializer


class CartProductRelationshipSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_cost = serializers.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        model = CartProductRelationship
        fields = ('id', 'created_at', 'product', 'count', 'total_cost',)
        read_only_fields = ('id', 'created_at',)


class CartSerializer(serializers.ModelSerializer):
    cart_products = CartProductRelationshipSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        model = Cart
        fields = ('id', 'created_at', 'cart_products', 'total_amount',)
        read_only_fields = ('id', 'created_at',)


class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id',)
        read_only_fields = ('id',)


class CartAddItemSerializer(serializers.ModelSerializer):
    cart = serializers.UUIDField(required=False)

    class Meta:
        model = CartProductRelationship
        fields = ('product', 'cart', 'count',)


class CartSetItemSerializer(serializers.ModelSerializer):
    cart = serializers.UUIDField(required=False)
    count = serializers.IntegerField(required=True)

    class Meta:
        model = CartProductRelationship
        fields = ('product', 'cart', 'count',)


class CartDeleteItemSerializer(serializers.ModelSerializer):
    cart = serializers.UUIDField(required=False)

    class Meta:
        model = CartProductRelationship
        fields = ('product', 'cart', 'count',)


class CartDeletePositionSerializer(serializers.ModelSerializer):
    cart = serializers.UUIDField(required=False)

    class Meta:
        model = CartProductRelationship
        fields = ('product', 'cart',)


class CartClearSerializer(serializers.ModelSerializer):
    cart = serializers.UUIDField(required=True)

    class Meta:
        model = CartProductRelationship
        fields = ('cart',)


class CreateCartPDFResponseSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'created_at', 'file',)
        read_only_fields = ('id', 'created_at',)

    def get_file(self, obj):
        filedest = create_pdf_cart(obj, context=self.context)
        return filedest
