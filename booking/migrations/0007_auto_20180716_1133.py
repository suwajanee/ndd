# Generated by Django 2.0.7 on 2018-07-16 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_booking_booking_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_color',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]
