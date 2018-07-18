# Generated by Django 2.0.7 on 2018-07-17 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_auto_20180717_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='principal',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='customer.Principal'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='shipper',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='customer.Shipper'),
        ),
    ]
