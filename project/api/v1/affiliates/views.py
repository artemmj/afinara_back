from django.utils.decorators import method_decorator

from rest_framework import permissions, viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.affiliates.models import Affiliate
from apps.helpers.exceptions import ErrorResponseSerializer
from .serializers import (
    AffiliateSerializer, AffiliateSlugsSerializer, AffiliateContactsSerializer,
    RequisiteSerializer,
)


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(responses={400: ErrorResponseSerializer})
)
class AffiliatesViewSet(ExtendedModelViewSet, CreateModelMixin, viewsets.GenericViewSet):
    queryset = Affiliate.objects.all().order_by('created_at')
    serializer_class = AffiliateSerializer
    serializer_class_map = {
        'list': AffiliateSlugsSerializer,
        'contacts': AffiliateContactsSerializer,
        'requisites': RequisiteSerializer,

    }
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'

    @action(['get'], detail=False, url_path='contacts', url_name='contacts')
    def contacts(self, request, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(['get'], detail=True, url_path='requisites', url_name='requisites')
    def requisites(self, request, **kwargs):
        affilate = self.get_object().requisite
        return Response(self.get_serializer(affilate).data)
