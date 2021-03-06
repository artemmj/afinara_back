# Generated by Django 3.0.2 on 2021-03-16 07:02

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
        ('affiliates', '0005_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='affiliate',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='director', to='affiliates.Affiliate', verbose_name='Филиал'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='affiliate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='employees', to='affiliates.Affiliate', verbose_name='Филиал'),
        ),
        migrations.AlterField(
            model_name='socialnetwork',
            name='affiliate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='social_networks', to='affiliates.Affiliate', verbose_name='Филиал'),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField()),
                ('affiliate', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='partners', to='affiliates.Affiliate', verbose_name='Филиал')),
                ('logo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='file.File', verbose_name='Лого')),
            ],
            options={
                'verbose_name': 'Партнер',
                'verbose_name_plural': 'Партнеры',
            },
        ),
    ]
