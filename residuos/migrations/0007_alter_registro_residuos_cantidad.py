# Generated by Django 5.0.4 on 2024-04-23 20:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residuos', '0006_alter_registro_residuos_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro_residuos',
            name='cantidad',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Cantidad'),
        ),
    ]
