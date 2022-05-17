import logging

from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.questionnaires.models import (
    Questionnaire, Question, QuestionnaireResult, Answer, QuestionCategory,
)
from api.v1.file.serializers import FileSerializer

logger = logging.getLogger()


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ('id', 'created_at', 'name', 'ordinal_number',)


class ReadAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'created_at', 'value',)


class WriteAnswerSerializer(serializers.ModelSerializer):
    value = serializers.JSONField()

    class Meta:
        model = Answer
        fields = ('id', 'value',)


class ReadQuestionSerializer(serializers.ModelSerializer):
    category = QuestionCategorySerializer()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('id', 'title', 'type', 'category', 'text_hint', 'answer')
        read_only_fields = ('id',)

    def get_answer(self, instance):
        answer = instance.answer_set.first()
        serializer = ReadAnswerSerializer(answer)
        return serializer.data


class ReadShortQuestionSerializer(serializers.ModelSerializer):
    category = QuestionCategorySerializer()

    class Meta:
        model = Question
        fields = ('id', 'ordinal_number', 'title', 'type', 'category', 'text_hint')
        read_only_fields = ('id',)


class WriteQuestionSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    answer = WriteAnswerSerializer()


class ShortQuestionnaireSerializer(serializers.ModelSerializer):
    template = FileSerializer()
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Questionnaire
        fields = ('id', 'title', 'template', 'questions_count')

    def get_questions_count(self, instance):
        return len(instance.questions.all())


class ReadQuestionnaireSerializer(serializers.ModelSerializer):
    template = FileSerializer()
    questions_count = serializers.SerializerMethodField()
    questions_categories = serializers.SerializerMethodField()

    class Meta:
        model = Questionnaire
        fields = (
            'id', 'created_at', 'title', 'template', 'questions_count',
            'questions_categories',
        )
        read_only_fields = ('id',)

    def get_questions_count(self, instance):
        return len(instance.questions.all())

    def get_questions_categories(self, instance):
        """ Разбить вопросы по категориям. """
        from collections import OrderedDict

        questions = instance.questions.all().order_by('ordinal_number')
        result_obj = OrderedDict()
        for q in questions:
            if not q.category:
                result_obj['non_category'] = list()
            else:
                result_obj[q.category.name] = list()

        for q in questions:
            serializer = ReadShortQuestionSerializer(q)
            data = serializer.data.copy()
            del data['category']
            if not q.category:
                result_obj['non_category'].append(data)
            else:
                result_obj[q.category.name].append(data)

        return result_obj


class WriteQuestionnaireSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField()
    questions = WriteQuestionSerializer(many=True)

    class Meta:
        model = Questionnaire
        fields = ('id', 'created_at', 'questions',)
        read_only_fields = ('id',)


class ReadQuestionnaireResultSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=True)
    full_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    questionnaire = ReadQuestionnaireSerializer()

    class Meta:
        model = QuestionnaireResult
        fields = (
            'id', 'created_at', 'full_name', 'phone', 'position',
            'questionnaire',
        )
        read_only_fields = ('id',)


class WriteQuestionnaireResultSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    position = serializers.CharField(required=False)
    questionnaire = WriteQuestionnaireSerializer()

    class Meta:
        model = QuestionnaireResult
        fields = (
            'id', 'created_at', 'full_name', 'phone', 'position',
            'questionnaire',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        # Берем шаблон из БД по айди, если нет - 404 NotFound
        template_questionnaire = get_object_or_404(
            Questionnaire,
            pk=validated_data['questionnaire']['id'],
        )

        # Создаем экземпляр опросника с ответами пользователя
        new_questionnaire = Questionnaire.objects.create(
            title=f'Результат опроса: {template_questionnaire.title}',
        )

        # Проверить, что кол-во ответов в запросе и шаблоне совпадает
        cnt_in_request = len(validated_data['questionnaire']['questions'])
        cnt_in_template = len(template_questionnaire.questions.all())
        if cnt_in_request != cnt_in_template:
            new_questionnaire.delete()
            error_msg = {
                'error': 'Количество вопросов о ответе не совпадает с таковым в шаблоне.',
                'detail': {
                    'count_in_request': cnt_in_request,
                    'count_in_template': cnt_in_template,
                }
            }
            logger.error(error_msg)
            raise ValidationError(error_msg)

        # Вопросы, на которые необходимо ответить /> валидировать их
        question_ids = [q_obj['id'] for q_obj in validated_data['questionnaire']['questions']]
        for i in range(0, len(question_ids)):
            for j in range(i+1, len(question_ids)):
                if question_ids[i] == question_ids[j]:
                    new_questionnaire.delete()
                    error_msg = {'error': 'В ответе обнаружены ответы с одинаковыми id\'s.'}
                    logger.error(error_msg)
                    raise ValidationError(error_msg)

        # Идем по всем вопросам в запросе, проверяя наличие в БД, проверяя
        # валидность jsonfield у answer'a (ответы необязательны, могу быть null)
        for q_obj in validated_data['questionnaire']['questions']:
            try:
                question = Question.objects.get(pk=q_obj['id'])
            except Question.DoesNotExist:
                new_questionnaire.delete()
                error_msg = {
                    'error': 'Не найден вопрос с таким id.',
                    'details': {'id': q_obj['id']},
                }
                logger.error(error_msg)
                raise ValidationError(error_msg)

            if 'data' not in q_obj['answer']['value']:
                new_questionnaire.delete()
                error_msg = {'error': 'Не найден ключ data в answer.value'}
                logger.error(error_msg)
                raise ValidationError(error_msg)

            # Проверяем соответствие типа ответа и пришедшего ответа
            question_type = question.type
            if q_obj['answer']['value']['data']:
                if (
                    (
                        question_type == Question.QuestionTypes.BOOL
                        and type(q_obj['answer']['value']['data']) is not bool
                    ) or
                    (
                        question_type == Question.QuestionTypes.TEXT
                        and type(q_obj['answer']['value']['data']) is not str
                    )
                ):
                    new_questionnaire.delete()
                    error_type = type(q_obj['answer']['value']['data'])
                    error_msg = {
                        'error': f'Обнаружено несответствие типов: нужно {question_type} / получено {error_type}.'
                    }
                    raise ValidationError(error_msg)

            quest_result, _ = QuestionnaireResult.objects.get_or_create(
                full_name=validated_data['full_name'],
                phone=validated_data['phone'],
                position=validated_data['position'] if 'position' in validated_data else None,
                questionnaire=new_questionnaire,
            )

            # Создаем новый вопрос для опросника
            new_question = Question.objects.create(
                type=question.type,
                title=question.title,
                questionnaire=new_questionnaire,
            )
            # Создаем ответ, привязываем все
            new_answer = Answer.objects.create(value=q_obj['answer']['value'])
            new_answer.question = new_question
            new_answer.questionnaire_result = quest_result
            new_answer.save()

        return quest_result
