# Generated by Django 3.0.2 on 2021-04-03 10:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
        ('catalog', '0003_auto_20210403_1030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='photos',
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_photos', to='file.File')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='catalog.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
