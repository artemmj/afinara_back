# Generated by Django 3.0.2 on 2021-04-07 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20210403_1048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productphoto',
            options={'verbose_name': 'Фото товара', 'verbose_name_plural': 'Фото товара'},
        ),
        migrations.AddField(
            model_name='catalog',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255, verbose_name='slug'),
        ),
    ]
