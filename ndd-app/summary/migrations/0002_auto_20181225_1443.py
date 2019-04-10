# Generated by Django 2.1 on 2018-12-25 07:43

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_remove_shipper_address'),
        ('summary', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='summarycustomer',
            old_name='customer',
            new_name='customer_custom',
        ),
        migrations.AddField(
            model_name='summarycustomer',
            name='customer_main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='customer.Principal'),
        ),
        migrations.AlterField(
            model_name='customerform',
            name='optional',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='formdetail',
            name='form_detail',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=15, null=True), size=6),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('0', '-'), ('1', 'Processing'), ('2', 'Finished')], default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='summarycustomer',
            name='status',
            field=models.CharField(choices=[('0', '-'), ('1', 'Processing'), ('2', 'Finished')], default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='summaryweek',
            name='status',
            field=models.CharField(choices=[('0', '-'), ('1', 'Processing'), ('2', 'Finished')], default=0, max_length=1),
        ),
    ]