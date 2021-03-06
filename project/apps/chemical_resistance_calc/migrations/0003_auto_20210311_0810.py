# Generated by Django 3.0.2 on 2021-03-11 08:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('chemical_resistance_calc', '0002_tableofchemicalresistance_formula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tableofchemicalresistance',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Название'),
        ),
        migrations.CreateModel(
            name='CalculatorCalculationRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('mail_or_phone', models.CharField(max_length=32, verbose_name='Почта или номер телефона')),
                ('chemical_resistance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='calc_result', to='chemical_resistance_calc.TableOfChemicalResistance')),
            ],
            options={
                'verbose_name': 'Запрос расчета хим. стойкости',
                'verbose_name_plural': 'Запросы расчета хим. стойкости',
            },
        ),
    ]
