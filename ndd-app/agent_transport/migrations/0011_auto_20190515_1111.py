# Generated by Django 2.2 on 2019-05-15 04:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent_transport', '0010_agenttransport_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agenttransport',
            old_name='color',
            new_name='detail',
        ),
    ]