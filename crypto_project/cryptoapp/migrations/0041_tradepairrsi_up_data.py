# Generated by Django 4.2.1 on 2024-05-26 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoapp', '0040_tradepairrsi_tradingpairrsi'),
    ]

    operations = [
        migrations.AddField(
            model_name='tradepairrsi',
            name='up_Data',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
