# Generated by Django 2.2 on 2019-05-15 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_auto_20190515_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='nextday',
            field=models.CharField(choices=[('2', 'ยกลง'), ('1', 'ตัดหาง'), ('0', '-')], default=0, max_length=1),
        ),
    ]
