# Generated by Django 2.2 on 2019-04-20 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent_transport', '0007_auto_20190403_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenttransport',
            name='status',
            field=models.CharField(choices=[('3', 'Pickup'), ('2', 'Finished'), ('1', '-'), ('0', 'Cancel')], default=1, max_length=1),
        ),
    ]