# Generated by Django 3.0.2 on 2021-06-11 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]