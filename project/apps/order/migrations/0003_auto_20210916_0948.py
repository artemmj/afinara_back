# Generated by Django 3.0.2 on 2021-09-16 06:48

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_remove_order_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email_or_phone',
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='Почта'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default='', max_length=128, region=None, verbose_name='Телефон'),
            preserve_default=False,
        ),
    ]
