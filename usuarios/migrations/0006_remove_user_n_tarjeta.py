# Generated by Django 3.1 on 2020-12-14 00:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_user_n_tarjeta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='N_tarjeta',
        ),
    ]
