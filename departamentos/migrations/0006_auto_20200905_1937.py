# Generated by Django 3.1 on 2020-09-05 23:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departamentos', '0005_auto_20200905_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arriendo',
            name='reserva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arriendo', to='departamentos.reserva'),
        ),
    ]
