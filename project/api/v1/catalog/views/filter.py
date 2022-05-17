from rest_framework import permissions, mixins
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.helpers.viewsets import ExtendedViewSet
from apps.catalog.models import Filter
from api.v1.catalog.serializers import FilterSerializer
from api.v1.catalog.filters import FilterFilterSet


class FilterViewSet(mixins.ListModelMixin, ExtendedViewSet):
    queryset = Filter.objects.all().order_by('ordinal_number')
    serializer_class = FilterSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = FilterFilterSet

    def list(self, request):
        serializer = self.get_serializer(self.filter_queryset(self.get_queryset()), many=True)
        return Response(serializer.data)
