# Generated by Django 2.1.5 on 2019-03-15 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent_transport', '0005_agenttransport_summary_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenttransport',
            name='agent',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='agenttransport',
            name='booking_no',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='agenttransport',
            name='pickup_from',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='agenttransport',
            name='remark',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='agenttransport',
            name='return_to',
            field=models.CharField(blank=True, default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='agenttransport',
            name='size',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
