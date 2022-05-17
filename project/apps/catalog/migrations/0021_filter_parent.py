# Generated by Django 3.0.2 on 2021-05-25 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_filter_ordinal_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='catalog.Filter', verbose_name='От кого зависит фильтр (опционально)'),
        ),
    ]