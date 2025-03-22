# Generated by Django 5.1.7 on 2025-03-20 02:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaccion',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaccion',
            name='producto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventario.producto'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='producto',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
