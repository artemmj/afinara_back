# Generated by Django 3.0.2 on 2021-06-11 14:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0003_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('delivery_type', models.CharField(choices=[('pickup', 'Самовывоз'), ('transport_company', 'Транспортная компания')], max_length=32, verbose_name='Тип доставки')),
                ('fio', models.CharField(max_length=64, verbose_name='Инициалы')),
                ('email_or_phone', models.CharField(max_length=32, verbose_name='Почта или номер телефона')),
                ('inn', models.CharField(max_length=16, verbose_name='ИНН')),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='cart.Cart')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
    ]
