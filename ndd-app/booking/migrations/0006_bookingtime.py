# Generated by Django 2.1.5 on 2019-03-06 04:43

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20181106_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_in_time', django.contrib.postgres.fields.jsonb.JSONField()),
                ('pickup_out_time', django.contrib.postgres.fields.jsonb.JSONField()),
                ('factory_in_time', django.contrib.postgres.fields.jsonb.JSONField()),
                ('factory_load_start_time', django.contrib.postgres.fields.jsonb.JSONField()),
                ('factory_load_finish_time', django.contrib.postgres.fields.jsonb.JSONField()),
                ('factory_out_time', django.contrib.postgres.fields.jsonb.JSONField()),
                ('return_in_time', django.contrib.postgres.fields.jsonb.JSONField()),
                ('return_out_time', django.contrib.postgres.fields.jsonb.JSONField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookingtimes', to='booking.Booking')),
            ],
        ),
    ]
