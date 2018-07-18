# Generated by Django 2.0.7 on 2018-07-17 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_auto_20180717_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='principal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Principal'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='shipper',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Shipper'),
        ),
    ]
