# Generated by Django 4.2.1 on 2024-02-17 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptoapp', '0021_dashbord_torgov_balance1_dashbord_torgov_balance2'),
    ]

    operations = [
        migrations.AddField(
            model_name='profitprice2',
            name='datadohod',
            field=models.DateTimeField(null=True),
        ),
    ]
