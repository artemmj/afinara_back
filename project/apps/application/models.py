from django.db import models
from apps.helpers.models import UUIDModel, CreatedModel
from phonenumber_field.modelfields import PhoneNumberField
from apps.file.models import File


class Application(UUIDModel, CreatedModel):
    name = models.CharField('Имя отправителя', max_length=150)
    phone = PhoneNumberField('Номер телефона', help_text='Пример, +79510549236')
    email = models.EmailField('Электронная почта', blank=True, default='')
    comment = models.CharField('Комментрий', max_length=200, default='')
    files = models.ManyToManyField(File, verbose_name='Файоы',
                                   related_name='files')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.name}'
