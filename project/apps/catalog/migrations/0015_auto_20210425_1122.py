# Generated by Django 3.0.2 on 2021-04-25 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20210421_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prodattr',
            name='text',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Символьное значение'),
        ),
    ]