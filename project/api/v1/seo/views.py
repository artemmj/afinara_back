from django.utils.decorators import method_decorator

from rest_framework import permissions

from drf_yasg.utils import swagger_auto_schema

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.seo.models import Seo
from .serializers import SeoSerializer
from apps.helpers.exceptions import ErrorResponseSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(responses={400: ErrorResponseSerializer})
)
class SeoViewSet(ExtendedModelViewSet):
    queryset = Seo.objects.all().order_by('created_at')
    serializer_class = SeoSerializer
    permission_classes = (permissions.AllowAny,)
