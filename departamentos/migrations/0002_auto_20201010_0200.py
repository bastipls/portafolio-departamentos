# Generated by Django 3.1 on 2020-10-10 05:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departamentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reserva', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventario',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventario', to='departamentos.departamento'),
        ),
        migrations.AddField(
            model_name='imagen',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='departamentos.departamento'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='check_out',
            name='arriendo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='check_out', to='departamentos.arriendo'),
        ),
        migrations.AddField(
            model_name='check_in',
            name='arriendo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='check_in', to='departamentos.arriendo'),
        ),
        migrations.AddField(
            model_name='arriendo',
            name='reserva',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='arriendo', to='departamentos.reserva'),
        ),
    ]
