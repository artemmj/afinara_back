# Generated by Django 3.0.2 on 2021-06-16 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0008_remove_catalog_product_catalogs'),
        ('catalog', '0025_auto_20210609_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='support_catalogs',
            field=models.ManyToManyField(related_name='products_support_catalog', to='support.Catalog'),
        ),
    ]
