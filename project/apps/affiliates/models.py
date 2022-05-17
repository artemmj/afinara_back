from uuid import uuid4

from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField
from ckeditor_uploader.fields import RichTextUploadingField

from apps.helpers.models import UUIDModel, CreatedModel, SLUGModel
from apps.file.models import File


def directory_path(instance, filename):
    return f'upload/{timezone.now().strftime("%Y/%m/%d")}/{uuid4()}{filename}'


class Requisite(UUIDModel, CreatedModel):
    name_requisite = models.CharField('Наименование реквизита филиала', max_length=200)
    full_name = models.CharField('Полное наименование реквизита филиала', max_length=200)
    legal_address = models.CharField('Юридический адрес', max_length=200)
    physical_address = models.CharField('Физический адрес', max_length=200)
    ogrn = models.CharField('ОГРН', max_length=50, blank=True, default='')
    inn = models.CharField('ИНН', max_length=50, blank=True, default='')
    kpp = models.CharField('КПП', max_length=50, blank=True, default='')
    okpo = models.CharField('ОКПО', max_length=50, blank=True, default='')
    okved = models.CharField('ОКВЭД', max_length=50, blank=True, default='')
    okato = models.CharField('ОКАТО', max_length=50, blank=True, default='')
    oktmo = models.CharField('ОКТМО', max_length=50, blank=True, default='')
    okfc = models.CharField('ОКФМ', max_length=50, blank=True, default='')
    payment_account = models.CharField('Расчетный счет', max_length=250)
    correspondent_account = models.CharField('Корересподентский счет', max_length=250)
    bik = models.CharField('БИК', max_length=50)

    class Meta:
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'

    def __str__(self):
        return self.name_requisite


class Affiliate(UUIDModel, CreatedModel, SLUGModel):
    class SlugTypes(models.TextChoices):
        afinara = 'afinara', 'afinara'
        atlant_a = 'atlant-a', 'atlant-a'
        a_mitra = 'a-mitra', 'a-mitra'
        a_sibra = 'a-sibra', 'a-sibra'
        arlanufa = 'arlanufa', 'arlanufa'

    name = models.CharField('Название филиала', max_length=64, unique=True)
    company_name = models.CharField('Название компании', max_length=128, null=True, blank=True)
    logo = models.ForeignKey(File, models.CASCADE, verbose_name='Логотип', related_name='logo')
    main_photo = models.ForeignKey(File, models.CASCADE, verbose_name='Главное фото', related_name='main_photo')
    phone_up = PhoneNumberField('Телефон в шапке')
    phone_down = PhoneNumberField('Телефон в подвале', null=True, blank=True)
    email = models.EmailField('E-mail')
    city = models.CharField('Город', max_length=64)
    address = models.CharField('Адрес', max_length=256)
    copyright = models.CharField('Копирайт', max_length=256)
    address_storage = models.CharField('Адрес склада', max_length=256)
    work_graphic_office = models.CharField('График работы офиса', max_length=200, blank=True, default='')
    work_graphic_storage = models.CharField('График работы склада', max_length=200, blank=True, default='')
    about = RichTextUploadingField('Статья о компании')
    slug = models.SlugField(
        verbose_name='slug',
        allow_unicode=True,
        max_length=255,
        blank=True,
        choices=SlugTypes.choices
    )
    domens = models.CharField('Домены для филиала, через запятую если несколько', max_length=512, null=True, blank=True)
    theme = models.CharField('Тема, класс оформления для филиала', max_length=128, null=True, blank=True)
    latitude = models.DecimalField(verbose_name='Широта', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(verbose_name='Долгота', max_digits=9, decimal_places=6, null=True, blank=True)
    latitude_storage = models.DecimalField(verbose_name='Широта склада', max_digits=9, decimal_places=6, null=True, blank=True)
    longitude_storage = models.DecimalField(verbose_name='Долгота склада', max_digits=9, decimal_places=6, null=True, blank=True)
    requisite = models.ForeignKey(Requisite, models.DO_NOTHING, null=True, verbose_name='Реквизиты филиала')

    class Meta:
        verbose_name = 'Филиал'
        verbose_name_plural = 'Филиалы'

    def __str__(self):
        return self.name


class TermsOfUseFiles(UUIDModel, CreatedModel):
    affiliate = models.OneToOneField(Affiliate, models.CASCADE, related_name='terms_of_use')
    terms_of_use_user = models.FileField(upload_to=directory_path, verbose_name='Пользовательское соглашение')
    terms_of_use_site = models.FileField(upload_to=directory_path, verbose_name='Условия пользования сайтом')


class Director(UUIDModel, CreatedModel):
    fio = models.CharField('ФИО', max_length=128)
    position = models.CharField('Должность', max_length=64)
    photo = models.ForeignKey(File, models.CASCADE, verbose_name='Фото')
    description = RichTextUploadingField('Описание')
    affiliate = models.OneToOneField(Affiliate, models.DO_NOTHING, verbose_name='Филиал', related_name='director')

    class Meta:
        verbose_name = 'Директор'
        verbose_name_plural = 'Директора'

    def __str__(self):
        return self.fio


class SocialNetwork(UUIDModel, CreatedModel):
    class Types(models.TextChoices):
        facebook = 'facebook', 'Facebook'
        vk = 'vk', 'ВКонтакте'
        youtube = 'youtube', 'YouTube'
        instagram = 'instagram', 'Instagram'
        twitter = 'twitter', 'Twitter'

    type = models.CharField('Тип', max_length=16, choices=Types.choices)
    link = models.URLField('Ссылка', max_length=256)
    affiliate = models.ForeignKey(Affiliate, models.DO_NOTHING, verbose_name='Филиал', related_name='social_networks')

    class Meta:
        verbose_name = 'Ссылка на соц. сеть'
        verbose_name_plural = 'Ссылки на соц. сети'

    def __str__(self):
        return f'{self.type}: {self.link}'


class Employee(UUIDModel, CreatedModel):
    fio = models.CharField('ФИО', max_length=128)
    position = models.CharField('Должность', max_length=64)
    photo = models.ForeignKey(File, models.CASCADE, verbose_name='Фото')
    affiliate = models.ForeignKey(Affiliate, models.DO_NOTHING, verbose_name='Филиал', related_name='employees')
    phone = PhoneNumberField('Телефон', null=True, blank=True)
    email = models.EmailField('Email', null=True, blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.fio


class Partner(UUIDModel, CreatedModel):
    logo = models.ForeignKey(File, models.DO_NOTHING, verbose_name='Лого')
    text = RichTextUploadingField()
    affiliate = models.ForeignKey(Affiliate, models.DO_NOTHING, verbose_name='Филиал', related_name='partners')

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'
