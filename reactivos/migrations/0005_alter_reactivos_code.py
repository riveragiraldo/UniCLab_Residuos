# Generated by Django 5.0.4 on 2024-06-07 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reactivos', '0004_alter_user_position_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reactivos',
            name='code',
            field=models.CharField(max_length=255, verbose_name='Código'),
        ),
    ]
