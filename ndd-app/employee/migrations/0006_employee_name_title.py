# Generated by Django 2.2 on 2019-11-23 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_auto_20191031_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='name_title',
            field=models.CharField(blank=True, default='', max_length=5, null=True),
        ),
    ]