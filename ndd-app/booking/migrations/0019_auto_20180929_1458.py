# Generated by Django 2.1 on 2018-09-29 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0018_auto_20180926_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='address',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='address_other',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='cancel',
        ),
        migrations.AddField(
            model_name='booking',
            name='fac_ndd',
            field=models.CharField(choices=[('1', 'Yes'), ('0', '-')], default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='booking',
            name='start',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('2', 'Finished'), ('1', '-'), ('0', 'Cancel')], default=0, max_length=1),
        ),
        migrations.AddField(
            model_name='booking',
            name='yard_ndd',
            field=models.CharField(choices=[('1', 'Yes'), ('0', '-')], default=0, max_length=1),
        ),
    ]
