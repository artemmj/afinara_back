# Generated by Django 3.0.2 on 2021-03-14 09:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('name', models.CharField(max_length=64, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория статьи',
                'verbose_name_plural': 'Категории статьи',
            },
        ),
        migrations.CreateModel(
            name='CatalogCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('name', models.CharField(max_length=64, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория каталога',
                'verbose_name_plural': 'Категории каталога',
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('description', models.TextField(max_length=512, verbose_name='Описание')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate_file', to='file.File', verbose_name='Файл')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate_photo', to='file.File', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Сертификат',
                'verbose_name_plural': 'Сертификаты',
            },
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('description', models.TextField(max_length=512, verbose_name='Описание')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.CatalogCategory', verbose_name='Категория')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog_file', to='file.File', verbose_name='Файл')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='catalog_photo', to='file.File', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Каталог',
                'verbose_name_plural': 'Каталоги',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('description', models.TextField(max_length=512, verbose_name='Описание')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='support.ArticleCategory', verbose_name='Категория')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_photo', to='file.File', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
