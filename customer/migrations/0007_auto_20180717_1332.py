# Generated by Django 2.0.7 on 2018-07-17 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0006_auto_20180717_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='principal',
            name='principal_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='shipper',
            name='shipper_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
