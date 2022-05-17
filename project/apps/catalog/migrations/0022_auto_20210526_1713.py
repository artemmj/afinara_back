# Generated by Django 3.0.2 on 2021-05-26 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_filter_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='parent_value',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Выбранное значение в родительском фильтре для активации текущего'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='catalog.Filter', verbose_name='От кого зависит фильтр'),
        ),
    ]
