# Generated by Django 5.0.4 on 2024-05-15 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residuos', '0021_solicitud_residuo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitud_residuo',
            name='registro_residuo',
        ),
        migrations.AddField(
            model_name='registro_residuos',
            name='registro_solicitud',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitud_residuos', to='residuos.solicitud_residuo'),
        ),
    ]
