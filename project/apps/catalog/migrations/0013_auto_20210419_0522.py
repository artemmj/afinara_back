# Generated by Django 3.0.2 on 2021-04-19 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20210419_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Название'),
        ),
    ]
