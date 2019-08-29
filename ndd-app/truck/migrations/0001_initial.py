# Generated by Django 2.2 on 2019-08-29 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0003_remove_job_starting_salary'),
    ]

    operations = [
        migrations.CreateModel(
            name='TruckManufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('category', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=5, null=True)),
                ('license_plate', models.CharField(blank=True, max_length=7, null=True)),
                ('tax_expired_date', models.DateField(blank=True, default=None, null=True)),
                ('pat_pass_expired_date', models.DateField(blank=True, default=None, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('driver', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employee.Driver')),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='truck.TruckManufacturer')),
            ],
        ),
        migrations.CreateModel(
            name='Chassis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=3, null=True)),
                ('license_plate', models.CharField(blank=True, max_length=7, null=True)),
                ('tax_expired_date', models.DateField(blank=True, default=None, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='truck.TruckManufacturer')),
            ],
        ),
    ]
