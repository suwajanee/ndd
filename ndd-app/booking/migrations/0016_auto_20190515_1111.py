# Generated by Django 2.2 on 2019-05-15 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_auto_20190514_1129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='color',
            new_name='detail',
        ),
    ]
