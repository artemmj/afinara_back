# Generated by Django 3.0.2 on 2021-05-21 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_auto_20210510_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='ordinal_number',
            field=models.IntegerField(default=0),
        ),
    ]