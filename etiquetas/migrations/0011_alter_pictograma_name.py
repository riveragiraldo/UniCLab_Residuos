# Generated by Django 5.0.4 on 2024-08-05 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etiquetas', '0010_pictograma_created_by_pictograma_date_create_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pictograma',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Nombre'),
        ),
    ]