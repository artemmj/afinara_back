# Generated by Django 3.0.2 on 2021-12-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0015_auto_20211220_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliate',
            name='latitude_storage',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Широта склада'),
        ),
        migrations.AddField(
            model_name='affiliate',
            name='longitude_storage',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='Долгота склада'),
        ),
    ]
