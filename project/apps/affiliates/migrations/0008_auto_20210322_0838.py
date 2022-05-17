# Generated by Django 3.0.2 on 2021-03-22 08:38

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0007_auto_20210316_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliate',
            name='city',
            field=models.CharField(default='', max_length=64, verbose_name='Город'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='employee',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Телефон'),
        ),
    ]