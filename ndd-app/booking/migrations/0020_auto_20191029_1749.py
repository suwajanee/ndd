# Generated by Django 2.2 on 2019-10-29 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0019_auto_20191021_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingtime',
            name='factory_in_time',
        ),
        migrations.RemoveField(
            model_name='bookingtime',
            name='factory_load_finish_time',
        ),
        migrations.RemoveField(
            model_name='bookingtime',
            name='factory_load_start_time',
        ),
        migrations.RemoveField(
            model_name='bookingtime',
            name='factory_out_time',
        ),
        migrations.RemoveField(
            model_name='bookingtime',
            name='pickup_in_time',
        ),
        migrations.RemoveField(
            model_name='bookingtime',
            name='pickup_out_time',
        ),
        migrations.RemoveField(
            model_name='bookingtime',
            name='return_in_time',
        ),
        migrations.RemoveField(
            model_name='bookingtime',
            name='return_out_time',
        ),
    ]