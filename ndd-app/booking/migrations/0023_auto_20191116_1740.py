# Generated by Django 2.2 on 2019-11-16 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0022_auto_20191114_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingtime',
            name='key',
        ),
        migrations.RemoveField(
            model_name='bookingtime',
            name='time',
        ),
    ]
