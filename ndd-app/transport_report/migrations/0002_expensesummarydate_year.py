# Generated by Django 2.2 on 2020-02-19 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0011_auto_20190605_1701'),
        ('transport_report', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensesummarydate',
            name='year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='summary.Year'),
        ),
    ]