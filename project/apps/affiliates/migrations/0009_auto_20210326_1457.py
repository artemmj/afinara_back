# Generated by Django 3.0.2 on 2021-03-26 14:57

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0008_auto_20210322_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Описание'),
        ),
    ]
