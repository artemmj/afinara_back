# Generated by Django 3.0.2 on 2021-05-28 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_product_description_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.CharField(blank=True, max_length=16, null=True, verbose_name='Материал'),
        ),
    ]
