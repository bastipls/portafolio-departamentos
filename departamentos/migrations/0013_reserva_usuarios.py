# Generated by Django 3.1 on 2020-09-12 23:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departamentos', '0012_auto_20200910_0307'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='usuarios',
            field=models.ManyToManyField(blank=True, related_name='reserva_historial', to=settings.AUTH_USER_MODEL),
        ),
    ]