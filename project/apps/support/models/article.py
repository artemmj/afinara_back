from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

from apps.file.models import File
from apps.helpers.models import UUIDModel, CreatedModel, SLUGModel


class ArticleCategory(UUIDModel, CreatedModel, SLUGModel):
    name = models.CharField('Категория', max_length=64)

    class Meta:
        verbose_name = 'Категория статьи'
        verbose_name_plural = 'Категории статьи'

    def __str__(self):
        return self.name


class Article(UUIDModel, CreatedModel, SLUGModel):
    category = models.ForeignKey(ArticleCategory, models.CASCADE, verbose_name='Категория')
    name = models.CharField('Название', max_length=64)
    description = models.TextField('Описание', max_length=512)
    photo = models.ForeignKey(File, models.CASCADE, verbose_name='Фото', related_name='article_main_photo')
    text = RichTextUploadingField()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.name


class ArticlePhoto(UUIDModel, CreatedModel):
    article = models.ForeignKey(Article, models.CASCADE, verbose_name='Статья', related_name='article_photos')
    photo = models.ForeignKey(File, models.CASCADE, verbose_name='Фото', related_name='article_photo')

    class Meta:
        verbose_name = 'Фото статьи'
        verbose_name_plural = 'Фото статьи'
