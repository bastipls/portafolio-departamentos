# Generated by Django 3.1 on 2020-09-20 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departamentos', '0017_auto_20200916_2031'),
    ]

    operations = [
        migrations.AddField(
            model_name='transporte',
            name='fecha_solicitud',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]