# Generated by Django 3.1 on 2020-12-13 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20201213_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='N_tarjeta',
        ),
    ]
