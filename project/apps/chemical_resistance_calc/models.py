from django.db import models

from apps.helpers.models import UUIDModel, CreatedModel


class TableOfChemicalResistance(UUIDModel):
    name = models.CharField('Название', max_length=256)
    formula = models.CharField('Формула', max_length=64, null=True, blank=True)
    state = models.CharField('Состояние', max_length=32, null=True, blank=True)
    concentration = models.CharField('Концентрация', max_length=32, null=True, blank=True)
    temperature = models.IntegerField('Температура', null=True, blank=True)

    # Материал корпуса
    pvh = models.IntegerField('ПВХ', null=True, blank=True)
    pp = models.IntegerField('ПП', null=True, blank=True)
    pvdf = models.IntegerField('ПВДФ', null=True, blank=True)
    hpvh = models.IntegerField('ХПВХ', null=True, blank=True)

    # Материал уплотнений
    nbr = models.IntegerField('NBR', null=True, blank=True)
    epdm = models.IntegerField('EPDM', null=True, blank=True)
    fmk = models.IntegerField('FMK', null=True, blank=True)
    ptfe = models.IntegerField('PTFE', null=True, blank=True)

    class Meta:
        verbose_name = 'ЭЛЕКТРОННАЯ ТАБЛИЦА ХИМИЧЕСКОЙ СТОЙКОСТИ'
        verbose_name_plural = 'ЭЛЕКТРОННАЯ ТАБЛИЦА ХИМИЧЕСКОЙ СТОЙКОСТИ'

    def __str__(self):
        return f'{self.name} ({self.formula}); {self.state}; {self.concentration}; {self.temperature}'


class CalculatorCalculationRequest(UUIDModel, CreatedModel):
    name = models.CharField('Имя', max_length=64)
    mail_or_phone = models.CharField('Почта или номер телефона', max_length=32)
    chemical_resistance = models.ForeignKey(
        TableOfChemicalResistance,
        models.SET_NULL,
        related_name='calc_result',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Запрос расчета хим. стойкости'
        verbose_name_plural = 'Запросы расчета хим. стойкости'
