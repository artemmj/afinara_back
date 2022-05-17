from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from apps.helpers.models import UUIDModel, CreatedModel
from apps.file.models import File


class Order(UUIDModel, CreatedModel):

    class DeliveryType(models.TextChoices):
        pickup = 'pickup', 'Самовывоз'
        transport_company = 'transport_company', 'Транспортная компания'

    delivery_type = models.CharField('Тип доставки', max_length=32, choices=DeliveryType.choices)
    fio = models.CharField('Инициалы', max_length=64)
    email = models.EmailField('Почта')
    phone = PhoneNumberField('Телефон')
    inn = models.CharField('ИНН', max_length=16, default='', blank=True)
    name_company = models.CharField('Название компании', max_length=100, default='', blank=True)
    comment = models.CharField('Комментарий', max_length=150, default='', blank=True)
    requisites = models.ManyToManyField(
        File,
        verbose_name='Реквизиты заказчика',
        related_name='requisites',
        blank=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.fio}, {self.email} -- {self.phone}'
