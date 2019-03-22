# Generated by Django 2.1 on 2018-12-03 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent_transport', '0002_remove_agenttransport_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenttransport',
            name='operation_type',
            field=models.CharField(choices=[('', '-'), ('export_loaded', 'Export Loaded'), ('import_loaded', 'Import Loaded'), ('export_empty', 'Export Empty'), ('import_loaded', 'Import Empty')], default='', max_length=15),
        ),
        migrations.AddField(
            model_name='agenttransport',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]