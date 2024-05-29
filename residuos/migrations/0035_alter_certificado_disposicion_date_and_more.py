# Generated by Django 5.0.4 on 2024-05-27 23:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residuos', '0034_certificado_disposicion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificado_disposicion',
            name='date',
            field=models.DateField(verbose_name='Fecha de Certificación'),
        ),
        migrations.CreateModel(
            name='InformacionInteres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Breve descripción o Título')),
                ('tipo', models.CharField(choices=[('Video de Youtube', 'Video de Youtube'), ('Enlace Externo', 'Enlace Externo'), ('Imagen en la Web', 'Imagen en la Web')], max_length=20, verbose_name='Tipo')),
                ('url', models.URLField(unique=True, verbose_name='URL')),
                ('date_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha Creación')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha Actualización')),
                ('is_active', models.BooleanField(default=True, help_text='Activo', verbose_name='Activo')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='createby_enlaces', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_enlaces', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Información de Interés',
                'verbose_name_plural': 'Información de Interés',
            },
        ),
    ]