# Generated by Django 2.2 on 2019-05-14 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_remove_booking_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('5', 'Return'), ('4', 'Factory'), ('3', 'Yard'), ('2', 'Completed'), ('1', '-'), ('0', 'Cancel')], default=1, max_length=1),
        ),
    ]
