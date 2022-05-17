from django.db import models

from apps.file.models import File
from apps.helpers.models import UUIDModel, CreatedModel, SLUGModel


class CatalogCategory(UUIDModel, CreatedModel, SLUGModel):
    name = models.CharField('Категория', max_length=64)
    order = models.SmallIntegerField('Порядковый номер отображения', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Категория каталога'
        verbose_name_plural = 'Категории каталога'

    def __str__(self):
        return self.name


class Catalog(UUIDModel, CreatedModel, SLUGModel):
    category = models.ForeignKey(CatalogCategory, models.CASCADE, verbose_name='Категория')
    name = models.CharField('Название', max_length=64)
    description = models.TextField('Описание', max_length=512)
    photo = models.ForeignKey(File, models.CASCADE, verbose_name='Фото', related_name='catalog_photo')
    file = models.ForeignKey(File, models.CASCADE, verbose_name='Файл', related_name='catalog_file')
    ordering_num = models.IntegerField('Порядковый номер', default=0)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    def __str__(self):
        return f'{self.category.name} -- {self.name}'
