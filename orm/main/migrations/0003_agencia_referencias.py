# Generated by Django 4.2.20 on 2025-04-13 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_agencia_colaborador_cotizacion_cuenta_empresa_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencia',
            name='referencias',
            field=models.TextField(default='[]', null=True),
        ),
    ]
