# Generated by Django 5.0.4 on 2024-06-07 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactivos', '0005_alter_reactivos_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactivos',
            name='cas',
            field=models.CharField(max_length=100, verbose_name='Código CAS'),
        ),
    ]
