# Generated by Django 2.2 on 2019-10-09 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_remove_job_starting_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='co',
            field=models.CharField(blank=True, default='ndd', max_length=5, null=True),
        ),
    ]