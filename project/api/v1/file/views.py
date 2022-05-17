from django.utils.decorators import method_decorator

from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema

from apps.file.models import File
from apps.helpers.batchmixin import DeleteBatchMixin
from apps.helpers.viewsets import ExtendedModelViewSet

from .serializers import FileSerializer
from apps.helpers.exceptions import ErrorResponseSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(responses={400: ErrorResponseSerializer})
)
class FileViewSet(ExtendedModelViewSet, DeleteBatchMixin):
    queryset = File.objects.all().non_deleted()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)
