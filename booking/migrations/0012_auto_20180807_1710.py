# Generated by Django 2.0.7 on 2018-08-07 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_booking_cancel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='cancel',
            field=models.CharField(choices=[('1', 'Cancel'), ('0', '-')], default=0, max_length=1),
        ),
    ]
