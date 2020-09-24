# Generated by Django 3.1 on 2020-09-24 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departamentos', '0020_auto_20200919_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.PositiveIntegerField()),
                ('descripcion', models.TextField(null=True)),
                ('duracion', models.TimeField(blank=True)),
                ('fecha', models.DateTimeField()),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tour', to='departamentos.reserva')),
            ],
        ),
    ]
