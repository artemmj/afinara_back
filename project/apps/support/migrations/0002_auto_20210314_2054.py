# Generated by Django 3.0.2 on 2021-03-14 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Название'),
        ),
    ]
