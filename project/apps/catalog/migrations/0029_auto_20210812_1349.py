# Generated by Django 3.0.2 on 2021-08-12 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0028_auto_20210622_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description_text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст в описании'),
        ),
    ]
