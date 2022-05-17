from django.utils.decorators import method_decorator

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from apps.helpers.viewsets import ExtendedModelViewSet
from apps.questionnaires.models import Questionnaire, QuestionnaireResult
from .serializers import (
    ReadQuestionnaireSerializer, WriteQuestionnaireResultSerializer, ReadQuestionnaireResultSerializer,
    ShortQuestionnaireSerializer,
)
from apps.helpers.exceptions import ErrorResponseSerializer


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(responses={400: ErrorResponseSerializer})
)
class QuestionnairesViewSet(ExtendedModelViewSet):
    serializer_class = ReadQuestionnaireSerializer
    serializer_class_map = {
        'list': ShortQuestionnaireSerializer,
    }
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Questionnaire.objects.all().distinct('title').exclude(
            title__icontains='Результат опроса:'
        )

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ReadQuestionnaireResultSerializer},
        request_body=WriteQuestionnaireResultSerializer,)
    @action(methods=['post'], detail=False, url_path='create-answer', url_name='create-answer')
    def create_answer(self, request):
        serializer = WriteQuestionnaireResultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        serializer = ReadQuestionnaireResultSerializer(obj)
        return Response(serializer.data)


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(responses={400: ErrorResponseSerializer})
)
class QuestionnaireResultViewSet(ExtendedModelViewSet):
    queryset = QuestionnaireResult.objects.all()
    serializer_class = ReadQuestionnaireResultSerializer
    permission_classes = (permissions.AllowAny,)
