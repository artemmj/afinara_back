from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.support.models import (
    Article, ArticleCategory, Catalog, CatalogCategory, Certificate,
)
from .serializers import (
    ArticleSerializer, ArticleCategorySerializer, SupportCatalogSerializer,
    CatalogCategorySerializer, CertificateSerializer,
)
from .filters import ArticleFilterSet, CatalogFilterSet


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'per_page'
    max_page_size = 1000


class ArticleViewSet(ExtendedModelViewSet):
    queryset = Article.objects.all().order_by('-created_at')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = ArticleFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    lookup_field = 'slug'


class ArticleCategoriesViewSet(ExtendedModelViewSet):
    queryset = ArticleCategory.objects.all().order_by('-created_at')
    serializer_class = ArticleCategorySerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    lookup_field = 'slug'
    pagination_class = LargeResultsSetPagination


class SupportCatalogViewSet(ExtendedModelViewSet):
    queryset = Catalog.objects.all().order_by('ordering_num')
    serializer_class = SupportCatalogSerializer
    permission_classes = (permissions.AllowAny,)
    filter_class = CatalogFilterSet
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    lookup_field = 'slug'


class CatalogCategoriesViewSet(ExtendedModelViewSet):
    queryset = CatalogCategory.objects.all()
    ordering_field = ['order']
    serializer_class = CatalogCategorySerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    lookup_field = 'slug'
    pagination_class = LargeResultsSetPagination


class CertificateViewSet(ExtendedModelViewSet):
    queryset = Certificate.objects.all().order_by('-created_at')
    serializer_class = CertificateSerializer
    permission_classes = (permissions.AllowAny,)
