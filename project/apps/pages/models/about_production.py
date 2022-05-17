from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

from apps.helpers.models import UUIDModel, CreatedModel, SLUGModel
from apps.file.models import File


class AboutProduction(UUIDModel, CreatedModel, SLUGModel):
    name = models.CharField('Название', max_length=120)
    preview_for_mainpage = models.ForeignKey(
        File,
        models.CASCADE,
        related_name='about_production_preview_for_mainpage',
        verbose_name='Превью для главной страницы',
        null=True,
        blank=True,
    )
    photo = models.ForeignKey(
        File,
        models.CASCADE,
        related_name='about_production_photo',
        verbose_name='Главное фото',
    )
    article = RichTextUploadingField('Статья')

    class Meta:
        verbose_name = 'Подробнее о продукции'
        verbose_name_plural = 'Подробнее о продукции'

    def __str__(self):
        return self.name
