# Generated by Django 5.0.4 on 2024-06-09 20:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactivos', '0006_alter_reactivos_cas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudesexternas',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reactivos.laboratorios', verbose_name='Laboratorio que recepciona'),
        ),
    ]
