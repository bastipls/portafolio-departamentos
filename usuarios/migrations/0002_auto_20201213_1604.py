# Generated by Django 3.1 on 2020-12-13 19:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='N_tarjeta',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(26)]),
        ),
    ]
