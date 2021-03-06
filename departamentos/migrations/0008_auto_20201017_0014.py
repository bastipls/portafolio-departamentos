# Generated by Django 3.1 on 2020-10-17 03:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departamentos', '0007_remove_departamento_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tour',
            name='dia',
            field=models.CharField(default=datetime.date(2020, 10, 17), max_length=50),
        ),
        migrations.AlterField(
            model_name='transporte',
            name='conductor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='transporte',
            name='hora',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transporte',
            name='vehiculo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
