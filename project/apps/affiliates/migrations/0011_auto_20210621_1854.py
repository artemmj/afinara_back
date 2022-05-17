# Generated by Django 3.0.2 on 2021-06-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliates', '0010_termsofusefiles'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliate',
            name='domens',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Домены для филиала, через запятую если несколько'),
        ),
        migrations.AddField(
            model_name='affiliate',
            name='theme',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Тема, класс оформления для филиала'),
        ),
        migrations.AlterField(
            model_name='affiliate',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, choices=[('afinara', 'afinara'), ('atlant-a', 'atlant-a'), ('a-mitra', 'a-mitra'), ('a-sibra', 'a-sibra'), ('arlanufa', 'arlanufa')], max_length=255, verbose_name='slug'),
        ),
    ]