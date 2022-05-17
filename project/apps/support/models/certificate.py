from django.db import models

from apps.file.models import File
from apps.helpers.models import UUIDModel, CreatedModel


class Certificate(UUIDModel, CreatedModel):
    name = models.CharField('Название', max_length=128)
    description = models.TextField('Описание', max_length=512)
    photo = models.ForeignKey(File, models.CASCADE, verbose_name='Фото', related_name='certificate_photo')
    file = models.ForeignKey(File, models.CASCADE, verbose_name='Файл', related_name='certificate_file')

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return self.name
