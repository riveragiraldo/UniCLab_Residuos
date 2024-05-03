# Generated by Django 5.0.4 on 2024-04-23 16:36

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactivos', '0001_initial'),
        ('residuos', '0003_clasificacion_residuos_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='REGISTRO_RESIDUOS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependencia', models.CharField(choices=[('Area', 'Área'), ('Laboratorio', 'Laboratorio')], max_length=11, verbose_name='Dependencia')),
                ('area', models.CharField(blank=True, max_length=200, null=True)),
                ('nombre_residuo', models.CharField(max_length=200, verbose_name='Nombre del Residuo')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cantidad')),
                ('numero_envases', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Número de Envases')),
                ('is_active', models.BooleanField(default=True, help_text='Activo', verbose_name='Activo')),
                ('date_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha Creación')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Actualización')),
                ('clasificado', models.ManyToManyField(to='residuos.clasificacion_residuos', verbose_name='Clasificado')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='createby_registro', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reactivos.estados', verbose_name='Estado')),
                ('laboratorio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reactivos.laboratorios')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_registro', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('unidades', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reactivos.unidades', verbose_name='Unidades')),
            ],
        ),
    ]