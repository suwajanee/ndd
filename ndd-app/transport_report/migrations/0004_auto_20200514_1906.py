# Generated by Django 2.2 on 2020-05-14 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport_report', '0003_variable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='total_expense',
        ),
        migrations.AddField(
            model_name='expense',
            name='co_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='expense',
            name='cus_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]