# Generated by Django 2.2 on 2019-05-14 04:29

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent_transport', '0009_auto_20190514_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenttransport',
            name='color',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]