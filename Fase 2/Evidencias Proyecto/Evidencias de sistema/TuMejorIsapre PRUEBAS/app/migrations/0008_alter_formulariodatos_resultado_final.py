# Generated by Django 5.1.1 on 2024-10-24 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_formulariodatos_monto_dispuesto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulariodatos',
            name='resultado_final',
            field=models.FloatField(default=0.0),
        ),
    ]
