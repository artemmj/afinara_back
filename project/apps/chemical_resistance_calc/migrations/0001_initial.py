# Generated by Django 3.0.2 on 2021-02-14 14:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TableOfChemicalResistance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название (формула)')),
                ('state', models.CharField(blank=True, max_length=32, null=True, verbose_name='Состояние')),
                ('concentration', models.CharField(blank=True, max_length=32, null=True, verbose_name='Концентрация')),
                ('temperature', models.IntegerField(blank=True, null=True, verbose_name='Температура')),
                ('pvh', models.IntegerField(blank=True, null=True, verbose_name='ПВХ')),
                ('pp', models.IntegerField(blank=True, null=True, verbose_name='ПП')),
                ('pvdf', models.IntegerField(blank=True, null=True, verbose_name='ПВДФ')),
                ('hpvh', models.IntegerField(blank=True, null=True, verbose_name='ХПВХ')),
                ('nbr', models.IntegerField(blank=True, null=True, verbose_name='NBR')),
                ('epdm', models.IntegerField(blank=True, null=True, verbose_name='EPDM')),
                ('fmk', models.IntegerField(blank=True, null=True, verbose_name='FMK')),
                ('ptfe', models.IntegerField(blank=True, null=True, verbose_name='PTFE')),
            ],
            options={
                'verbose_name': 'ЭЛЕКТРОННАЯ ТАБЛИЦА ХИМИЧЕСКОЙ СТОЙКОСТИ',
                'verbose_name_plural': 'ЭЛЕКТРОННАЯ ТАБЛИЦА ХИМИЧЕСКОЙ СТОЙКОСТИ',
            },
        ),
    ]
