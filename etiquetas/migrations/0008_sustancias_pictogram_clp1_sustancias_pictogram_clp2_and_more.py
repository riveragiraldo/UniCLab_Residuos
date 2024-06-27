# Generated by Django 5.0.4 on 2024-06-26 19:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etiquetas', '0007_pictograma'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustancias',
            name='pictogram_clp1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictograma_clp1', to='etiquetas.pictograma', verbose_name='Pictograma CLP 1'),
        ),
        migrations.AddField(
            model_name='sustancias',
            name='pictogram_clp2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictograma_clp2', to='etiquetas.pictograma', verbose_name='Pictograma CLP 2'),
        ),
        migrations.AddField(
            model_name='sustancias',
            name='pictogram_clp3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictograma_clp3', to='etiquetas.pictograma', verbose_name='Pictograma CLP 3'),
        ),
        migrations.AddField(
            model_name='sustancias',
            name='pictogram_clp4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictograma_clp4', to='etiquetas.pictograma', verbose_name='Pictograma CLP 4'),
        ),
        migrations.AddField(
            model_name='sustancias',
            name='pictogram_clp5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictograma_clp5', to='etiquetas.pictograma', verbose_name='Pictograma CLP 5'),
        ),
        migrations.AddField(
            model_name='sustancias',
            name='pictogram_clp6',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pictograma_clp6', to='etiquetas.pictograma', verbose_name='Pictograma CLP 6'),
        ),
    ]
