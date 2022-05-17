from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.application.serializers import ApplicationSerializer
from apps.application.models import Application
from apps.application.tasks import send_email_feedback_task
from apps.helpers.viewsets import ExtendedViewSet


class ApplicationViewSet(ExtendedViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (AllowAny,)

    @action(methods=['POST'], detail=False, url_path='send-feedback', url_name='send-feedback')
    def send_feedback(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appl = serializer.save()
        send_email_feedback_task.delay(appl.pk)
        return Response(serializer.data)
