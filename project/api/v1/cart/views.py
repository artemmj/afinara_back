from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.cart.models import Cart
from api.v1.order.serializers import CreateOrderSerializer
from .serializers import (
    CartSerializer, CartCreateSerializer, CartAddItemSerializer,
    CartSetItemSerializer, CartDeleteItemSerializer,
    CartDeletePositionSerializer, CartClearSerializer,
    CreateCartPDFResponseSerializer
)
from .services import (
    AddItemToCartService, SetItemToCartService,
    DeleteItemFromCartServise, DeletePositionFromCartService,
    ClearCartService,
)


class CartViewSet(ExtendedModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (permissions.AllowAny,)
    serializer_class_map = {
        'create': CartCreateSerializer,
        'add_item': CartAddItemSerializer,
        'set_item': CartSetItemSerializer,
        'delete_item': CartDeleteItemSerializer,
        'delete_position': CartDeletePositionSerializer,
        'clear_cart': CartClearSerializer,
        'create_order': CreateOrderSerializer,
        'create_cart_pdf': CreateCartPDFResponseSerializer,
    }

    @swagger_auto_schema(request_body=CartAddItemSerializer, responses={200: CartAddItemSerializer})
    @action(methods=['post'], detail=True, url_path=r'add-item')
    def add_item(self, request, pk=None, **kwargs):
        request_data = request.data.copy()
        request_data['cart'] = self.get_object().id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        cart = AddItemToCartService.execute(serializer.data)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CartSetItemSerializer, responses={200: CartSetItemSerializer})
    @action(methods=['post'], detail=True, url_path=r'set-item')
    def set_item(self, request, pk=None, **kwargs):
        request_data = request.data.copy()
        request_data['cart'] = self.get_object().id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        cart = SetItemToCartService.execute(serializer.data)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CartDeleteItemSerializer, responses={200: CartDeleteItemSerializer})
    @action(methods=['post'], detail=True, url_path=r'delete-item')
    def delete_item(self, request, pk=None, **kwargs):
        request_data = request.data.copy()
        request_data['cart'] = self.get_object().id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        cart = DeleteItemFromCartServise.execute(serializer.data)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CartDeletePositionSerializer, responses={200: CartDeletePositionSerializer})
    @action(methods=['post'], detail=True, url_path=r'delete-position')
    def delete_position(self, request, pk=None, **kwargs):
        request_data = request.data.copy()
        request_data['cart'] = self.get_object().id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        cart = DeletePositionFromCartService.execute(serializer.data)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CartClearSerializer, responses={200: CartClearSerializer})
    @action(methods=['post'], detail=True, url_path=r'clear-cart')
    def clear_cart(self, request, pk=None, **kwargs):
        request_data = request.data.copy()
        request_data['cart'] = self.get_object().id
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        cart = ClearCartService.execute(serializer.data)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CreateOrderSerializer, responses={200: CreateOrderSerializer})
    @action(methods=['post'], detail=True, url_path=r'create-order')
    def create_order(self, request, pk=None, **kwargs):
        request_data = request.data.copy()
        request_data['cart'] = self.get_object().id
        serializer = CreateOrderSerializer(
            data=request_data,
            context={
                "cart_id": self.get_object().id,
                "request": request,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: CreateCartPDFResponseSerializer})
    @action(methods=['get'], detail=True, url_path=r'create-pdf')
    def create_cart_pdf(self, request, pk=None, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)
