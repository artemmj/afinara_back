# Generated by Django 3.0.2 on 2021-03-10 17:34

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('name', models.CharField(max_length=64, verbose_name='Название филиала')),
                ('phone_up', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон в шапке')),
                ('phone_down', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Телефон в подвале')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('address', models.CharField(max_length=256, verbose_name='Адрес')),
                ('copyright', models.CharField(max_length=256, verbose_name='Копирайт')),
                ('address_storage', models.CharField(max_length=256, verbose_name='Адрес склада')),
                ('about', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Статья о компании')),
                ('logo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logo', to='file.File', verbose_name='Логотип')),
                ('main_photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_photo', to='file.File', verbose_name='Главное фото')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
        ),
        migrations.CreateModel(
            name='SocialNetwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('type', models.CharField(choices=[('facebook', 'Facebook'), ('vk', 'ВКонтакте'), ('youtube', 'YouTube'), ('instagram', 'Instagram'), ('twitter', 'Twitter')], max_length=16, verbose_name='Тип')),
                ('link', models.URLField(max_length=256, verbose_name='Ссылка')),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_networks', to='affiliates.Affiliate', verbose_name='Филиал')),
            ],
            options={
                'verbose_name': 'Ссылка на соц. сеть',
                'verbose_name_plural': 'Ссылки на соц. сети',
            },
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('fio', models.CharField(max_length=128, verbose_name='ФИО')),
                ('position', models.CharField(max_length=64, verbose_name='Должность')),
                ('description', models.CharField(max_length=1024, verbose_name='Описание')),
                ('affiliate', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='director', to='affiliates.Affiliate', verbose_name='Филиал')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file.File', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Директор',
                'verbose_name_plural': 'Директора',
            },
        ),
    ]
