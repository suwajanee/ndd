# Generated by Django 2.1 on 2018-10-11 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipperAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(blank=True, default='', max_length=50)),
                ('address', models.CharField(blank=True, default='', max_length=500)),
                ('shipper', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Shipper')),
            ],
        ),
    ]
