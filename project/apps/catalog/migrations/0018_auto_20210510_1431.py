# Generated by Django 3.0.2 on 2021-05-10 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0017_sizechart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sizechart',
            name='title',
            field=models.CharField(max_length=48, verbose_name='Название характеристики'),
        ),
        migrations.AlterField(
            model_name='sizechart',
            name='value',
            field=models.CharField(max_length=48, verbose_name='Значение характеристики'),
        ),
    ]
