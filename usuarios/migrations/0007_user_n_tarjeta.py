# Generated by Django 3.1 on 2020-12-14 00:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_remove_user_n_tarjeta'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='N_tarjeta',
            field=models.IntegerField(null=True, validators=[django.core.validators.MaxValueValidator(17)]),
        ),
    ]