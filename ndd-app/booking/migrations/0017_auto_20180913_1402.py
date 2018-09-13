# Generated by Django 2.1 on 2018-09-13 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_auto_20180912_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='factory_in_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='factory_load_finish_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='factory_load_start_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='factory_out_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='pickup_in_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='pickup_out_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='ref',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='booking',
            name='return_in_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='booking',
            name='return_out_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
