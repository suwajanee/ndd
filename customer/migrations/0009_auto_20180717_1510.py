# Generated by Django 2.0.7 on 2018-07-17 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_auto_20180717_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='principal',
            old_name='principal_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='shipper',
            old_name='shipper_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='shipper',
            old_name='principal_name',
            new_name='principal',
        ),
    ]
