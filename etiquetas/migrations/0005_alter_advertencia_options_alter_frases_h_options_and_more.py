# Generated by Django 5.0.4 on 2024-06-26 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('etiquetas', '0004_alter_advertencia_name_alter_frases_h_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertencia',
            options={'verbose_name': 'Advertencia', 'verbose_name_plural': 'Advertencias'},
        ),
        migrations.AlterModelOptions(
            name='frases_h',
            options={'verbose_name': 'Frase H', 'verbose_name_plural': 'Frases H'},
        ),
        migrations.AlterModelOptions(
            name='sustancias',
            options={'verbose_name': 'Sustancia', 'verbose_name_plural': 'Sustancias'},
        ),
    ]