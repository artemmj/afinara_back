# Generated by Django 3.0.2 on 2021-12-13 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_requisites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='inn',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='order',
            name='name_company',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Название компании'),
        ),
    ]
