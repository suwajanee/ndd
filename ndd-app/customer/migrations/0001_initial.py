# Generated by Django 2.1 on 2018-09-29 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Principal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('work_type', models.CharField(choices=[('normal', 'Normal'), ('agent-transport', 'Agent Transport')], default='normal', max_length=20)),
                ('cancel', models.CharField(choices=[('1', 'Cancel'), ('0', '-')], default=0, max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Shipper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200)),
                ('address', models.CharField(blank=True, default='', max_length=500)),
                ('cancel', models.CharField(choices=[('1', 'Cancel'), ('0', '-')], default=0, max_length=1)),
                ('principal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shippers', to='customer.Principal')),
            ],
        ),
    ]
