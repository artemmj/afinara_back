from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from drf_yasg.utils import swagger_auto_schema

from apps.helpers.viewsets import ExtendedViewSet, paginate_response
from apps.catalog.models import Product

from ..serializers import (
    ProductSerializer, ProductDetailSerializer,
    ProductPrintAssortmentSerializer, ProductPrintAssortmentResponseSerializer,
    ProductPrintSizeChartSerializer, ProductPrintSizeChartResponseSerializer,
)
from ..filters import ProductFilterSet
from ..helpers import sort_or_display_queryset
from .. import services


class ProductViewSet(mixins.RetrieveModelMixin, ExtendedViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    serializer_class_map = {
        'list': ProductSerializer,
        'retrieve': ProductDetailSerializer,
        'print_pdf_assortment': ProductPrintAssortmentSerializer,
        'print_pdf_size_chart': ProductPrintSizeChartSerializer,
    }
    permission_classes = (permissions.AllowAny,)
    ordering_fields = ('name', 'price')
    search_fields = ['name', 'full_name', 'vendor_code']
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_class = ProductFilterSet

    def list(self, request: Request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = sort_or_display_queryset(request.query_params.copy(), queryset)
        if not queryset:
            raise NotFound()
        return paginate_response(self, queryset)

    @swagger_auto_schema(
        method='POST',
        request_body=ProductPrintAssortmentSerializer(),
        responses={200: ProductPrintAssortmentResponseSerializer()},
    )
    @action(methods=['POST'], detail=False, url_path='print-assortment', url_name='print_assortment')
    def print_pdf_assortment(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = services.get_pdf_assortment_filepath(serializer.data['product_id'], request)
        return Response({'file': result})

    @swagger_auto_schema(
        method='POST',
        request_body=ProductPrintSizeChartSerializer(),
        responses={200: ProductPrintSizeChartResponseSerializer()},
    )
    @action(methods=['POST'], detail=False, url_path='print-size-chart', url_name='print_size_chart')
    def print_pdf_size_chart(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = services.make_size_chart_pdf(serializer.data['product_id'], request)
        return Response({'file': result})
