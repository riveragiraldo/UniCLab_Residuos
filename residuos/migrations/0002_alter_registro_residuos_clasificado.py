# Generated by Django 5.0.4 on 2024-06-17 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residuos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registro_residuos',
            name='clasificado',
            field=models.ManyToManyField(blank=True, null=True, to='residuos.clasificacion_residuos', verbose_name='Clasificado'),
        ),
    ]