# Generated by Django 3.0.2 on 2021-03-16 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0006_auto_20210316_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliate',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=255, verbose_name='slug'),
        ),
    ]
