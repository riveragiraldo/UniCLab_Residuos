# Generated by Django 5.0.4 on 2024-05-15 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('residuos', '0024_alter_solicitud_residuo_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud_residuo',
            name='name',
            field=models.CharField(default='Sol', max_length=10),
        ),
    ]