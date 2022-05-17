from django.db import models

from apps.helpers.models import UUIDModel, CreatedModel


class MailRecipient(UUIDModel, CreatedModel):
    email = models.EmailField(unique=True)
    enabled = models.BooleanField('Включен в рассылку', default=True)

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'

    def __str__(self):
        return self.email
