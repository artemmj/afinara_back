from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import mixins

from apps.helpers.viewsets import ExtendedViewSet, paginate_response
from apps.catalog.models import Catalog

from ..serializers import CatalogSerializer, CatalogMainSerializer
from ..filters import CatalogFilterSet


class CatalogViewSet(mixins.ListModelMixin, ExtendedViewSet):
    queryset = Catalog.objects.all().order_by('ordering_num')
    serializer_class = CatalogSerializer
    serializer_class_map = {
        'main': CatalogMainSerializer,
    }
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_class = CatalogFilterSet
    lookup_field = 'slug'

    @action(['get'], detail=False)
    def main(self, request, *args, **kwargs):
        return paginate_response(
            self,
            self.get_queryset().filter(parent__isnull=True, show_on_mainpage=True),
        )
