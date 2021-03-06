# Generated by Django 3.0.2 on 2021-03-15 17:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
        ('affiliates', '0004_auto_20210315_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('fio', models.CharField(max_length=128, verbose_name='ФИО')),
                ('position', models.CharField(max_length=64, verbose_name='Должность')),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='affiliates.Affiliate', verbose_name='Филиал')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file.File', verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
    ]
