# Generated by Django 2.1 on 2018-09-26 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent_transport', '0007_auto_20180913_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenttransport',
            name='work_number',
            field=models.IntegerField(default=1),
        ),
    ]
