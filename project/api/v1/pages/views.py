from django.utils.decorators import method_decorator

from rest_framework import permissions

from drf_yasg.utils import swagger_auto_schema

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.pages.models import SolutionForArea, AboutProduction
from .serializers import SolutionForAreaSerializer, AboutProductionSerializer, ShortSolutionForAreaSerializer
from apps.helpers.exceptions import ErrorResponseSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(responses={400: ErrorResponseSerializer})
)
class SolutionForAreaViewSet(ExtendedModelViewSet):
    queryset = SolutionForArea.objects.all().order_by('created_at')
    serializer_class = SolutionForAreaSerializer
    serializer_class_map = {
        'list': ShortSolutionForAreaSerializer,
    }
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'


class AboutProductionViewSet(ExtendedModelViewSet):
    queryset = AboutProduction.objects.all().order_by('created_at')
    serializer_class = AboutProductionSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'
