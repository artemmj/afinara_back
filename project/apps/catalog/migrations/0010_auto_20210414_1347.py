# Generated by Django 3.0.2 on 2021-04-14 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_auto_20210412_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Название'),
        ),
    ]