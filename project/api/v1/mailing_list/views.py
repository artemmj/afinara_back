from django.utils.decorators import method_decorator

from rest_framework import permissions

from drf_yasg.utils import swagger_auto_schema

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.mailing_list.models import MailRecipient
from .serializers import MailRecipientSerializer
from apps.helpers.exceptions import ErrorResponseSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(responses={400: ErrorResponseSerializer})
)
class MailRecipientViewSet(ExtendedModelViewSet):
    queryset = MailRecipient.objects.all()
    serializer_class = MailRecipientSerializer
    permission_classes = (permissions.AllowAny,)
