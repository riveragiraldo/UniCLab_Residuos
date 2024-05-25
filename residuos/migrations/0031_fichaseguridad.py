# Generated by Django 5.0.4 on 2024-05-24 20:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residuos', '0030_solicitud_residuo_respondido_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaSeguridad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Nombre')),
                ('url', models.URLField(max_length=500, verbose_name='URL')),
                ('date_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha Creación')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='createby_fichaseguiridad', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_fichaseguiridad', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Ficha de Seguridad',
                'verbose_name_plural': 'Fichas de Seguridad',
            },
        ),
    ]
