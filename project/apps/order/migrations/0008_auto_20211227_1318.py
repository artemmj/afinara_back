# Generated by Django 3.0.2 on 2021-12-27 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20211213_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=150, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='inn',
            field=models.CharField(blank=True, default='', max_length=16, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='order',
            name='name_company',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Название компании'),
        ),
    ]