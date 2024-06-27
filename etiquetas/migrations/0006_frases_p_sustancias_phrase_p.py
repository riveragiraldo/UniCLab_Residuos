# Generated by Django 5.0.4 on 2024-06-26 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etiquetas', '0005_alter_advertencia_options_alter_frases_h_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frases_P',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Frase P',
                'verbose_name_plural': 'Frases P',
            },
        ),
        migrations.AddField(
            model_name='sustancias',
            name='phrase_p',
            field=models.ManyToManyField(blank=True, to='etiquetas.frases_p', verbose_name='Frases P'),
        ),
    ]
