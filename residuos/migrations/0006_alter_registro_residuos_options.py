# Generated by Django 5.0.4 on 2024-04-23 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('residuos', '0005_alter_registro_residuos_nombre_residuo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='registro_residuos',
            options={'verbose_name': 'Registro de Residuos', 'verbose_name_plural': 'Registros de Residuos'},
        ),
    ]
