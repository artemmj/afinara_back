import jsonfield

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.models import UUIDModel, CreatedModel
from apps.file.models import File


class Questionnaire(UUIDModel, CreatedModel):
    """
    Опросник, точнее шаблон опросника, на него ссылается результат опроса.
    """
    title = models.CharField(max_length=512)
    template = models.ForeignKey(
        File,
        models.CASCADE,
        verbose_name='Файл опросного листа',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Опросник'
        verbose_name_plural = 'Опросники'

    def __str__(self):
        return self.title


class QuestionCategory(UUIDModel, CreatedModel):
    """
    Объекты вопросов могут относиться к какой-то категории (а могут и нет).
    """
    name = models.CharField('Название', max_length=128)
    ordinal_number = models.PositiveSmallIntegerField('Порядковый номер', default=1)

    class Meta:
        verbose_name = 'Категория вопросов'
        verbose_name_plural = 'Категории вопросов'

    def __str__(self):
        return self.name


class Question(UUIDModel, CreatedModel):
    """ Объект вопроса, содержащий информацию о нем. """

    class QuestionTypes(models.TextChoices):
        BOOL = 'boolean', 'Выбрать вариант ответа'
        TEXT = 'text', 'Ответ текстом'

    type = models.CharField(
        'Тип вопроса',
        max_length=16,
        choices=QuestionTypes.choices,
        default=QuestionTypes.TEXT,
    )
    title = models.CharField(max_length=4096)
    category = models.ForeignKey(
        QuestionCategory,
        models.CASCADE,
        verbose_name='Категория',
        null=True,
        blank=True,
    )
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions')
    ordinal_number = models.PositiveSmallIntegerField('Порядковый номер', default=1)
    text_hint = models.CharField('Текст подсказки', max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return f'{self.id} / {self.title}'


class QuestionnaireResult(UUIDModel, CreatedModel):
    """
    Результат опроса - содержит инфу об ответившем + key на шаблон опросника.
    """
    full_name = models.CharField('Инициалы', max_length=128)
    phone = PhoneNumberField('Номер телефона')
    position = models.CharField('Должность', max_length=128, null=True, blank=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Результат опроса'
        verbose_name_plural = 'Результаты опроса'

    def __str__(self):
        return f'{self.full_name} / {self.phone}: {self.questionnaire.title}'


class Answer(UUIDModel, CreatedModel):
    """
    Объект ответа, содержит jsonfield из-за разных возможных вариантов ответа.
    """
    value = jsonfield.JSONField('Ответ на вопрос, в формате json')
    question = models.ForeignKey(
        Question, models.CASCADE, verbose_name='Вопрос', null=True, blank=True
    )
    questionnaire_result = models.ForeignKey(
        QuestionnaireResult, models.CASCADE, verbose_name='Результат опроса', null=True, blank=True
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return str(self.value)
