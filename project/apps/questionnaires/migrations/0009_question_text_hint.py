# Generated by Django 3.0.2 on 2021-03-04 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaires', '0008_question_ordinal_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='text_hint',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Текст подсказки'),
        ),
    ]
