# Generated by Django 2.0 on 2018-01-27 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_synonyms'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='synonyms',
            field=models.TextField(default=' ', null=True),
        ),
    ]