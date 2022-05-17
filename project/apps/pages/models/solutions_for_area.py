from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

from apps.helpers.models import UUIDModel, CreatedModel, SLUGModel
from apps.file.models import File
from apps.catalog.models import Product


class SolutionForArea(UUIDModel, CreatedModel, SLUGModel):
    name = models.CharField('Название', max_length=120)
    photo = models.ForeignKey(
        File, models.CASCADE, related_name='solution_for_area_photo', verbose_name='Главное фото',
    )
    article = RichTextUploadingField('Статья')
    products = models.ManyToManyField(Product, verbose_name='Товары', related_name='solution_products')

    class Meta:
        verbose_name = 'Решение для областей'
        verbose_name_plural = 'Решения для областей'

    def __str__(self):
        return self.name


class CompleteProject(UUIDModel, CreatedModel):
    title = models.CharField('Заголовок', max_length=120)
    text = RichTextUploadingField('Текст')
    photo = models.ForeignKey(
        File, models.CASCADE, related_name='complete_project', verbose_name='Фото',
    )
    solution_for_area = models.ForeignKey(
        SolutionForArea, models.CASCADE, related_name='complete_projects', verbose_name='Решение для области',
    )

    class Meta:
        verbose_name = 'Готовый проект'
        verbose_name_plural = 'Готовые проекты'

    def __str__(self):
        return self.title
