# Generated by Django 3.1 on 2020-10-19 11:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departamentos', '0009_auto_20201018_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='dia',
            field=models.CharField(default=datetime.date(2020, 10, 19), max_length=50),
        ),
    ]
