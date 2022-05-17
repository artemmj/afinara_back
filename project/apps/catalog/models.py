import random

from django.core.exceptions import ValidationError
from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField

from apps.helpers.models import UUIDModel, CreatedModel, SLUGModel
from apps.file.models import File
from apps.helpers.services import transliterate
from apps.support.models import Catalog as support_catalog


class Catalog(UUIDModel, CreatedModel, SLUGModel):
    name = models.CharField('Название', max_length=128)
    parent = models.ForeignKey('self', models.CASCADE, related_name='childs', null=True, blank=True)
    photo = models.ForeignKey(File, models.CASCADE, related_name='calatog_photo', null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    show_on_mainpage = models.BooleanField('Показывать на главной странице', default=False)
    ordering_num = models.IntegerField('Порядковый номер', default=1)

    class Meta:
        verbose_name = 'Каталог'
        verbose_name_plural = 'Каталоги'

    def __str__(self):
        if self.parent:
            return f'{self.parent.name}: {self.name}'
        return self.name

    def create_update_slug(self, obj):
        objs = self.__class__.objects.filter(name=obj.name).order_by('slug')
        if objs:
            if len(objs) == 1:
                self.slug = f'{transliterate(obj.name).lower()}-1'
            else:
                try:
                    slug_number = int(objs.last().slug.split('-')[-1])
                except Exception:
                    slug_number = random.randint(10, 99)
                self.slug = f'{transliterate(obj.name).lower()}-{slug_number + 1}'
        else:
            self.slug = f'{transliterate(obj.name).lower()}'

        if self.parent:
            self.slug = f'{self.parent.slug}_{self.slug}'


class Attribute(UUIDModel, CreatedModel, SLUGModel):
    class AttrTypes(models.TextChoices):
        FLOAT = 'float', 'Численный'
        CHAR = 'char', 'Символьный'

    name = models.CharField('Название', max_length=64, unique=True)
    type = models.CharField('Тип', max_length=16, choices=AttrTypes.choices)

    class Meta:
        verbose_name = 'Аттрибут'
        verbose_name_plural = 'Аттрибуты'

    def __str__(self):
        return f'{self.name} ({self.type})'


class Product(UUIDModel, CreatedModel):
    vendor_code = models.CharField('Артикул', max_length=64, unique=True)
    name = models.CharField('Наименование', max_length=256)
    full_name = models.TextField('Полное наименование товара', max_length=1024, null=True, blank=True)
    photos = models.ManyToManyField(File, verbose_name='Фото товара', related_name='products')

    price = models.FloatField('Цена', null=True, blank=True)
    material = models.CharField('Материал', max_length=16, null=True, blank=True)
    measure = models.CharField('Единица измерения', max_length=16, null=True, blank=True)
    description_text = models.TextField('Текст в описании', null=True, blank=True)
    catalog = models.ForeignKey(Catalog, models.CASCADE, related_name='products', verbose_name='Каталог')
    support_catalogs = models.ManyToManyField(
        support_catalog,
        related_name='products_support_catalog',
        verbose_name='Каталоги-файлы, ссылающиеся на этот товар',
        blank=True,
    )
    display_in_top_wo_catalog = models.BooleanField(
        'Отображать товар в топе, без выбранного каталога',
        default=False,
    )
    display_in_top_in_parent = models.BooleanField(
        'Отображать товар в топе, в каталоге первого уровня',
        default=False,
    )
    display_in_top_in_child = models.BooleanField(
        'Отображать товар в топе, в каталоге второго уровня',
        default=False,
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.vendor_code} - {self.name}'

    @property
    def fullname_with_attrs(self):
        name = self.name
        if diameters := self.attributes.filter(attribute__name='Диаметр'):
            try:
                if diameters[0].text[0].isnumeric():
                    name += f' d{int(float(diameters[0].text))}'
                else:
                    name += f' {int(float(diameters[0].text))}'
            except Exception:
                name += f' {diameters[0].text}'
        if pressures := self.attributes.filter(attribute__name='SDR - давление'):
            name += f' {pressures[0].text}'
        return name


class ProdAttr(UUIDModel, CreatedModel):
    attribute = models.ForeignKey(Attribute, models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, models.CASCADE, related_name='attributes')
    # В зависимости от type у attribute
    numeric = models.FloatField('Числовое значение', null=True, blank=True)
    text = models.CharField('Символьное значение', max_length=512, null=True, blank=True)
    text_translit = models.CharField('Транслит', max_length=1024, null=True, blank=True)

    class Meta:
        verbose_name = 'Товар-аттрибут'
        verbose_name_plural = 'Товары-аттрибуты'

    def save(self, *args, **kwargs):
        self.text_translit = transliterate(self.text)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} / {self.attribute.name} : {self.text}'


class Filter(UUIDModel, CreatedModel):

    class Type(models.TextChoices):
        CHOICE = 'choice', 'выбор'
        MULTI_CHOICE = 'multi_choice', 'мультивыбор'
        RANGE = 'range', 'диапазон'

    name = models.CharField('Название', max_length=64)
    catalog = models.ForeignKey(Catalog, models.CASCADE, related_name='filters', null=True, blank=True)
    attribute = models.ForeignKey(Attribute, models.CASCADE, related_name='filters', null=True)
    type = models.CharField('Тип фильтра', choices=Type.choices, max_length=14, null=True)
    ordinal_number = models.IntegerField(default=0)
    parent = models.ForeignKey(
        'self',
        models.CASCADE,
        verbose_name='От кого зависит фильтр (родительский фильтр)',
        related_name='childs',
        null=True,
        blank=True,
    )
    parent_value = models.CharField(
        'Выбранное значение в родительском фильтре для активации текущего',
        max_length=64,
        null=True,
        blank=True,
    )
    limitation_filter = models.ForeignKey(
        'self',
        models.CASCADE,
        verbose_name='Ограничивающий фильтр, от выбора которого будут фильтроваться варианты текущего фильтра',
        related_name='limitation_filters',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'

    def __str__(self):
        return f'{self.catalog}; {self.name} ({self.attribute.name})'

    def clean(self):
        super().clean()
        types = {
            Attribute.AttrTypes.FLOAT: {Filter.Type.RANGE},
            Attribute.AttrTypes.CHAR: {Filter.Type.MULTI_CHOICE, Filter.Type.CHOICE},
        }
        if self.type not in types[self.attribute.type]:
            raise ValidationError(f'Неверный тип фильтра для атрибута {self.attribute}')


class SizeChart(UUIDModel, CreatedModel):
    """ Таблица для хранения размерных характеристик у продукта. """
    product = models.ForeignKey(Product, models.CASCADE, related_name='size_chart')
    title = models.CharField('Название характеристики', max_length=64)
    value = models.CharField('Значение характеристики', max_length=64)

    class Meta:
        verbose_name = 'Размерная хакартеристика'
        verbose_name_plural = 'Размерные характеристики'

    def __str__(self):
        return f'{self.product.name}: {self.title} - {self.value}'
