# Generated by Django 4.0.6 on 2022-07-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_asset_tx_hashes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(max_length=500),
        ),
    ]
