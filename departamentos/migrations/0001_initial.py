# Generated by Django 3.1 on 2020-10-10 05:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Arriendo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Check_in',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diferencia', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Check_out',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(blank=True, choices=[('Aceptado', 'Aceptado'), ('Rechazado', 'Rechazado')], max_length=20, null=True)),
                ('valor_danos', models.PositiveIntegerField(verbose_name='Valor daños')),
                ('valor_transporte', models.PositiveIntegerField()),
                ('valor_tours', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mantencion', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('titulo', models.CharField(max_length=50, null=True)),
                ('banos', models.PositiveIntegerField(null=True, verbose_name='baños')),
                ('dormitorios', models.PositiveIntegerField(null=True)),
                ('descripcion', models.TextField(null=True)),
                ('direccion', models.CharField(max_length=60)),
                ('estado_mantencion', models.BooleanField(blank=True, default=True, null=True)),
                ('imagen', models.ImageField(blank=True, upload_to='departamentos_principal/%Y/%m')),
                ('precio', models.PositiveIntegerField(null=True)),
                ('metros_cuadrados', models.PositiveIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(null=True, upload_to='departamentos/%Y/%m')),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('Buen estado', 'Buen estado'), ('Mal estado', 'Mal estado')], default='Buen estado', max_length=20, null=True)),
                ('precio', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acompanantes', models.PositiveIntegerField(blank=True, null=True, verbose_name='acompañantes')),
                ('llegada', models.BooleanField(default=False)),
                ('dia_llegada', models.DateField(blank=True, null=True)),
                ('abono', models.PositiveIntegerField()),
                ('dias_estadia', models.PositiveIntegerField(verbose_name='días estadia')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reserva', to='departamentos.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_solicitud', models.DateField(auto_now=True, null=True)),
                ('estado_verificado', models.BooleanField(blank=True, null=True)),
                ('precio', models.PositiveIntegerField(default=10000)),
                ('desde', models.CharField(max_length=50)),
                ('hacia', models.CharField(max_length=50)),
                ('hora', models.TimeField(blank=True, null=True)),
                ('vehiculo', models.CharField(blank=True, max_length=50, null=True)),
                ('conductor', models.CharField(blank=True, max_length=50, null=True)),
                ('reserva', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='transporte', to='departamentos.reserva')),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('dia', models.CharField(blank=True, max_length=50, null=True)),
                ('duracion', models.PositiveIntegerField()),
                ('direccion', models.CharField(blank=True, max_length=50, null=True)),
                ('precio', models.PositiveIntegerField()),
                ('descripcion', models.TextField(null=True)),
                ('departamento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tour', to='departamentos.departamento')),
                ('reserva', models.ManyToManyField(blank=True, related_name='tour', to='departamentos.Reserva')),
            ],
        ),
    ]
