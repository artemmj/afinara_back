# Generated by Django 3.0.2 on 2021-02-26 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
        ('questionnaires', '0004_auto_20210220_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='file.File', verbose_name='Файл опросного листа'),
        ),
    ]
